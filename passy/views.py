from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpRequest
from django.http import HttpResponse
from django.shortcuts import render

from . import models


def index(request: HttpRequest) -> HttpResponse:

    context = dict()

    return render(request, 'passy/index.html', context)


def register(request: HttpRequest) -> HttpResponse:
    return HttpResponse("Register.")


def login(request: HttpRequest) -> HttpResponse:

    error_message = None

    if request.method == "POST":

        username: str = request.POST['username']
        master_password: str = request.POST['master_password']

        user = auth.authenticate(username=username, password=master_password)
        if user is None:
            error_message = "Bad Credentials"
            is_logged_in = False
        else:
            auth.login(request, user)
            is_logged_in = True
            request.session['master_password'] = master_password

    else:
        user: models.User = request.user
        is_logged_in = user.is_authenticated

    context = dict(is_logged_in=is_logged_in, error_message=error_message)

    return render(request, 'passy/login.html', context)


@login_required
def passwords(request: HttpRequest) -> HttpResponse:

    user: models.User = request.user
    error_message = None

    master_password = request.session['master_password']

    if request.method == "POST":
        site: str = request.POST['site']
        stored_password_text: str = request.POST['stored_password_text']

        stored_password = models.StoredPassword(site=site, owner=user)
        stored_password.set(password=stored_password_text, master_password=master_password)

        try:
            stored_password.save()
        except IntegrityError:
            error_message = f"Password for '{site}' already exists!"

    stored_passwords = models.get_passwords(owner=user)

    context = dict(stored_passwords=stored_passwords, error_message=error_message)

    return render(request, 'passy/passwords.html', context)


@login_required
def password(request: HttpRequest, site: str) -> HttpResponse:

    user: models.User = request.user

    master_password = request.session['master_password']

    stored_password = models.get_password(owner=user, site=site)
    stored_password_value = stored_password.get(master_password=master_password)

    context = dict(stored_password=stored_password, stored_password_value=stored_password_value)

    return render(request, 'passy/password.html', context)
