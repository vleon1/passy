from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpRequest
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect

from . import models


def index(request: HttpRequest) -> HttpResponse:
    return render(request, 'passy/index.html', dict())


def register(request: HttpRequest) -> HttpResponse:
    return HttpResponse("Register.")


def login(request: HttpRequest) -> HttpResponse:

    context = dict()

    if request.method == "POST":

        username: str = request.POST['username']
        master_password: str = request.POST['master_password']

        user = auth.authenticate(username=username, password=master_password)
        if user is not None:
            auth.login(request, user)
            request.session['master_password'] = master_password
            return redirect('passy:index')
        else:
            if models.User.objects.filter(username=username).exists():
                context['error_message'] = f"Provided password is incorrect for user '{username}'"
            else:
                context['error_message'] = f"User with the name '{username}' does not Exist!"

    return render(request, 'passy/login.html', context)


def logout(request: HttpRequest) -> HttpResponse:

    auth.logout(request)

    return redirect('passy:index')


@login_required
def passwords(request: HttpRequest) -> HttpResponse:

    user: models.User = request.user

    context = dict()

    if request.method == "POST":

        master_password = request.session['master_password']

        site: str = request.POST['site']
        stored_password_text: str = request.POST['stored_password_text']

        stored_password = models.StoredPassword(site=site, owner=user)
        stored_password.set(password=stored_password_text, master_password=master_password)

        try:
            stored_password.save()
        except IntegrityError:
            context['error_message'] = f"Password for '{site}' already exists!"

    context['stored_passwords'] = models.get_passwords(owner=user)

    return render(request, 'passy/passwords.html', context)


@login_required
def password(request: HttpRequest, site: str) -> HttpResponse:

    user: models.User = request.user
    master_password = request.session['master_password']

    stored_password = models.get_password(owner=user, site=site)

    if request.method == "POST":

        should_delete = request.POST.get("should_delete")
        if should_delete is not None:
            stored_password.delete()
            return redirect('passy:passwords')

        site: str = request.POST['site']
        stored_password_text: str = request.POST['stored_password_text']

        stored_password.site = site
        stored_password.set(password=stored_password_text, master_password=master_password)

        stored_password.save()

    else:
        stored_password_text = stored_password.get(master_password=master_password)

    if request.META['HTTP_ACCEPT'] == 'application/json':
        return JsonResponse(data=dict(password=stored_password_text))

    else:
        context = dict(stored_password=stored_password, stored_password_text=stored_password_text)
        return render(request, 'passy/password.html', context)
