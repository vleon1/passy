from django.contrib import auth
from django.contrib.auth.decorators import login_required

from django.http import HttpResponse, JsonResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View

from . import models, forms
import common.status

import common.typing


def redirect(name: str) -> HttpResponse:
    url = reverse(name)
    response = HttpResponseRedirect(url)
    response.status_code = common.status.HTTP_303_SEE_OTHER
    return response


def index(request: common.typing.Request) -> HttpResponse:
    return render(request, 'passy/index.html', dict())


def register(request: common.typing.Request) -> HttpResponse:
    return render(request, 'passy/register.html', dict())


class LoginView(View):

    template_name = 'passy/login.html'

    def get(self, request: common.typing.Request) -> HttpResponse:
        return render(request, self.template_name, dict())

    def post(self, request: common.typing.Request) -> HttpResponse:

        form = forms.Login(data=request.POST)

        if form.is_valid():

            username = form.cleaned_data['username']
            master_password = form.cleaned_data['master_password']

            user = auth.authenticate(username=username, password=master_password)
            if user is not None:

                auth.login(request, user)
                request.session['master_password'] = master_password
                return redirect('passy:password_list')

            user = models.get_user_or_none(username=username)
            if user is not None:
                if not user.is_active:
                    form.add_error(field=None, error=f"The user '{username}' is not activated yet")
                else:
                    form.add_error(field="master_password", error="Incorrect password")
            else:
                form.add_error(field="username", error="Incorrect username")

        return render(request, self.template_name, dict(form=form))


def logout(request: common.typing.Request) -> HttpResponse:

    auth.logout(request)

    return redirect('passy:index')


@method_decorator(login_required, name='dispatch')
class PasswordListView(View):

    template_name = 'passy/password_list.html'

    def post(self, request: common.typing.Request) -> HttpResponse:

        form = forms.StoredPassword(data=request.POST)

        if not form.create_model(request):
            pass  # todo: do something?

        return self.finalize_result(request)

    def get(self, request: common.typing.Request) -> HttpResponse:

        return self.finalize_result(request)

    def finalize_result(self, request: common.typing.Request) -> HttpResponse:

        form = forms.StoredPassword()

        form_data = {field.name: field.value() or "" for field in form}

        data = dict(stored_passwords=models.get_passwords(owner=request.user))
        data.update(form_data)

        return render(request, self.template_name, data)


@method_decorator(login_required, name='dispatch')
class PasswordView(View):

    template_name = 'passy/password.html'

    @staticmethod
    def get_object(request: common.typing.Request, pk: str) -> models.StoredPassword:
        return models.get_password(owner=request.user, pk=int(pk))

    def patch(self, request: common.typing.Request, pk: str) -> HttpResponse:

        instance = self.get_object(request, pk)

        form = forms.StoredPassword.from_request_and_instance(request=request, instance=instance)

        if form.update_model(request, instance):
            return redirect('passy:password_list')
        else:
            # todo: make sure we show the errors
            return self.finalize_result(request, instance, form)

    def get(self, request: common.typing.Request, pk: str) -> HttpResponse:

        instance = self.get_object(request, pk)

        form = forms.StoredPassword.from_request_and_instance(request=request, instance=instance)

        if request.is_ajax():
            return JsonResponse(data=form.data, status=common.status.HTTP_200_OK)
        else:
            return self.finalize_result(request, instance, form)

    def delete(self, request: common.typing.Request, pk: str) -> HttpResponse:

        instance = self.get_object(request, pk)

        instance.delete()

        return redirect('passy:password_list')

    def finalize_result(self, request: common.typing.Request, instance: models.StoredPassword, form: forms.StoredPassword) -> HttpResponse:

        data = dict(pk=instance.pk)
        data.update(form.data)

        return render(request, self.template_name, data)


class GetRandomPasswordView(View):

    @staticmethod
    def get(request: common.typing.Request) -> HttpResponse:

        form = forms.GeneratedPasswordRequest(data=request.GET)
        if form.is_valid():
            return JsonResponse(data=dict(generated_password=form.get_random_password()))
        else:
            return JsonResponse(data=form.errors)
