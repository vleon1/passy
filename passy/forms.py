import json

from django.db import IntegrityError
from django import forms

from . import models
import common.crypto

import common.typing


class StoredPassword(forms.Form):

    site = forms.CharField(max_length=models.MAX_CHAR_FIELD, required=True)
    stored_password_text = forms.CharField(initial=common.crypto.generate_random_password, required=True)

    @classmethod
    def from_request_and_instance(cls, request: common.typing.Request, instance: models.StoredPassword) -> "StoredPassword":

        request_data = json.loads(request.body) if request.body else dict()

        site = request_data.get("site") or instance.site
        stored_password_text = request_data.get("stored_password_text") or instance.get(master_password=request.session['master_password'])

        final_data = dict(site=site, stored_password_text=stored_password_text)

        return cls(data=final_data)

    def create_model(self, request: common.typing.Request) -> bool:

        instance = models.StoredPassword()

        return self.update_model(request, instance)

    def update_model(self, request: common.typing.Request, instance: models.StoredPassword) -> bool:

        if not self.is_valid():
            return False

        instance.site = self.cleaned_data['site']
        instance.owner = request.user

        instance.set(self.cleaned_data['stored_password_text'], request.session['master_password'])

        if models.StoredPassword.objects.filter(owner=request.user, site=instance.site).exists():
            self.add_error(field='site', error="This name is already used to for another password")
            return False
        else:
            instance.save()

        return True


class GeneratedPasswordRequest(forms.Form):

    length = forms.IntegerField(initial=common.crypto.default_password_length, required=True)
    use_symbols = forms.BooleanField(initial=True, required=False)

    def get_random_password(self) -> str:
        return common.crypto.generate_random_password(length=self.cleaned_data['length'],
                                                      use_symbols=self.cleaned_data['use_symbols'])


class Login(forms.Form):

    username = forms.CharField(max_length=models.MAX_CHAR_FIELD, required=True)
    master_password = forms.CharField(required=True)
