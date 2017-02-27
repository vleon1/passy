from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.core.handlers.wsgi import WSGIRequest

from django.http import HttpResponse, JsonResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View
from rest_framework import status
from rest_framework.request import Request
from rest_framework.reverse import reverse
from rest_framework.views import APIView

from . import models, serializers


def redirect(name: str, request: Request) -> HttpResponse:
    url = reverse(name, request=request)
    response = HttpResponseRedirect(url)
    response.status_code = status.HTTP_303_SEE_OTHER
    return response


def index(request: WSGIRequest) -> HttpResponse:
    return render(request, 'passy/index.html', dict())


def register(request: WSGIRequest) -> HttpResponse:
    return render(request, 'passy/register.html', dict())


def login(request: WSGIRequest) -> HttpResponse:

    context = dict()

    if request.method == "POST":

        username: str = request.POST['username']
        master_password: str = request.POST['master_password']

        user = auth.authenticate(username=username, password=master_password)
        if user is not None:
            auth.login(request, user)
            request.session['master_password'] = master_password
            return redirect('passy:index', request=request)
        else:
            if models.User.objects.filter(username=username).exists():
                context['error_message'] = f"Provided password is incorrect for user '{username}'"
            else:
                context['error_message'] = f"User with the name '{username}' does not Exist!"

    return render(request, 'passy/login.html', context)


def logout(request: WSGIRequest) -> HttpResponse:

    auth.logout(request)

    return redirect('passy:index', request=request)


@method_decorator(login_required, name='dispatch')
class PasswordListView(APIView):

    template_name = 'passy/password_list.html'

    def post(self, request: Request) -> HttpResponse:

        serializer = serializers.StoredPassword(request=request, data=request.data)

        if serializer.is_valid():
            serializer.save()

        return self.finalize_result(request, serializer)

    def get(self, request: Request) -> HttpResponse:

        serializer = serializers.StoredPassword(request=request)

        return self.finalize_result(request, serializer)

    def finalize_result(self, request: Request, serializer: serializers.StoredPassword) -> HttpResponse:

        get_password_serializer = serializers.GeneratedPasswordRequest()

        data = dict(stored_passwords=models.get_passwords(owner=request.user))
        data.update(serializer.data)
        data.update(get_password_serializer.data)

        return render(request, self.template_name, data)


@method_decorator(login_required, name='dispatch')
class PasswordView(APIView):

    template_name = 'passy/password.html'

    @staticmethod
    def get_object(request: Request, pk: str) -> models.StoredPassword:
        return models.get_password(owner=request.user, pk=int(pk))

    def patch(self, request: Request, pk: str) -> HttpResponse:

        instance = self.get_object(request, pk)

        serializer = serializers.StoredPassword(request=request, instance=instance, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return redirect('passy:passwords', request=request)
        else:
            return self.finalize_result(request, instance, serializer)

    def get(self, request: Request, pk: str) -> HttpResponse:

        instance = self.get_object(request, pk)

        serializer = serializers.StoredPassword(request=request, instance=instance)

        if request.is_ajax():
            return JsonResponse(data=serializer.data, status=status.HTTP_200_OK)
        else:
            return self.finalize_result(request, instance, serializer)

    def delete(self, request: Request, pk: str) -> HttpResponse:

        instance = self.get_object(request, pk)

        instance.delete()

        return redirect('passy:passwords', request=request)

    def finalize_result(self, request: Request, instance: models.StoredPassword, serializer: serializers.StoredPassword) -> HttpResponse:

        data = dict(pk=instance.pk)
        data.update(serializer.data)

        return render(request, self.template_name, data)


class GetRandomPasswordView(View):

    @staticmethod
    def get(request: WSGIRequest) -> HttpResponse:

        serializer = serializers.GeneratedPasswordRequest(data=request.GET)
        if serializer.is_valid():
            return JsonResponse(data=dict(generated_password=serializer.save()))
        else:
            return JSONResponse(data=serializer.errors)
