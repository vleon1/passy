from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View

from passy import forms
from passy import models

from passy.helpers import shortcuts
from passy.helpers import status
from passy.helpers import typing


class IndexView(View):

    template_name = 'passy/index.html'

    def get(self, request: typing.Request) -> HttpResponse:
        return render(request, self.template_name, dict())


class RegisterView(View):

    template_name = 'passy/register.html'

    def get(self, request: typing.Request) -> HttpResponse:
        return self.finalize_result(request, forms.Register())

    def post(self, request: typing.Request) -> HttpResponse:
        return self.finalize_result(request, forms.Register())

    def finalize_result(self, request: typing.Request, form: forms.Register) -> HttpResponse:
        return render(request, self.template_name, dict(form=form))


class LoginView(View):

    template_name = 'passy/login.html'

    def get(self, request: typing.Request) -> HttpResponse:

        return self.finalize_result(request, forms.Login())

    def post(self, request: typing.Request) -> HttpResponse:

        form = forms.Login(data=request.POST)

        if form.is_valid():

            username = form.cleaned_data['username']
            master_password = form.cleaned_data['master_password']

            user = auth.authenticate(username=username, password=master_password)
            if user is not None:

                auth.login(request, user)
                request.session['master_password'] = master_password
                return shortcuts.redirect('passy:password_list')

            user = models.get_user_or_none(username=username)
            if user is not None:
                if not user.is_active:
                    form.add_error(field=None, error=f"The user '{username}' is not activated yet")
                else:
                    form.add_error(field="master_password", error="Incorrect password")
            else:
                form.add_error(field="username", error="Incorrect username")

        return self.finalize_result(request, form)

    def finalize_result(self, request: typing.Request, form: forms.Login) -> HttpResponse:

        return render(request, self.template_name, dict(form=form))


class LogoutView(View):

    @staticmethod
    def post(request: typing.Request) -> HttpResponse:

        auth.logout(request)

        return shortcuts.redirect('passy:index')


@method_decorator(login_required, name='dispatch')
class PasswordListView(View):

    template_name = 'passy/password_list.html'

    def post(self, request: typing.Request) -> HttpResponse:

        form = forms.StoredPassword(data=request.POST)
        form.create_model(request)

        return self.finalize_result(request, form)

    def get(self, request: typing.Request) -> HttpResponse:

        return self.finalize_result(request, forms.StoredPassword())

    def finalize_result(self, request: typing.Request, form: forms.StoredPassword) -> HttpResponse:

        generated_password_request_form = forms.GeneratedPasswordRequest()

        data = dict(stored_passwords=models.get_passwords(owner=request.user),
                    password_form=form,
                    generated_password_request_form=generated_password_request_form)

        return render(request, self.template_name, data)


@method_decorator(login_required, name='dispatch')
class PasswordView(View):

    template_name = 'passy/password.html'

    @staticmethod
    def get_object(request: typing.Request, pk: str) -> models.StoredPassword:
        return models.get_password(owner=request.user, pk=int(pk))

    def patch(self, request: typing.Request, pk: str) -> HttpResponse:

        instance = self.get_object(request, pk)

        form = forms.StoredPassword.from_request_and_instance(request=request, instance=instance)

        if form.update_model(request, instance):
            return shortcuts.redirect('passy:password_list')
        else:
            # todo: make sure we show the errors
            return self.finalize_result(request, instance, form)

    def get(self, request: typing.Request, pk: str) -> HttpResponse:

        instance = self.get_object(request, pk)

        form = forms.StoredPassword.from_request_and_instance(request=request, instance=instance)

        if request.is_ajax():
            return JsonResponse(data=form.to_dict(), status=status.HTTP_200_OK)
        else:
            return self.finalize_result(request, instance, form)

    def delete(self, request: typing.Request, pk: str) -> HttpResponse:

        instance = self.get_object(request, pk)

        instance.delete()

        return shortcuts.redirect('passy:password_list')

    def finalize_result(self, request: typing.Request, instance: models.StoredPassword, form: forms.StoredPassword) -> HttpResponse:

        generated_password_request_form = forms.GeneratedPasswordRequest()

        data = dict(pk=instance.pk, password_form=form, generated_password_request_form=generated_password_request_form)

        return render(request, self.template_name, data)


@method_decorator(login_required, name='dispatch')
class GetRandomPasswordView(View):

    @staticmethod
    def get(request: typing.Request) -> HttpResponse:

        form = forms.GeneratedPasswordRequest(data=request.GET)
        if form.is_valid():
            return JsonResponse(data=dict(generated_password=form.get_random_password()), status=status.HTTP_200_OK)
        else:
            return JsonResponse(data=form.errors, status=status.HTTP_400_BAD_REQUEST)
