import json

from django import forms

from . import models
import common.crypto
import common.forms

import common.typing


class StoredPassword(common.forms.ComfyForm):

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

        return self.update_model(request, instance, check_for_existing_user=True)

    def update_model(self, request: common.typing.Request, instance: models.StoredPassword, check_for_existing_user: bool = False) -> bool:

        if not self.is_valid():
            return False

        instance.site = self['site']
        instance.owner = request.user

        instance.set(self['stored_password_text'], request.session['master_password'])

        if check_for_existing_user and models.StoredPassword.objects.filter(owner=request.user, site=instance.site).exists():
            self.add_error(field='site', error=f"This name {instance.site} is already used for another password")
            return False
        else:
            instance.save()

        return True


class GeneratedPasswordRequest(common.forms.ComfyForm):

    length = forms.IntegerField(initial=common.crypto.default_password_length, required=True)
    use_symbols = forms.BooleanField(initial=True, required=False)

    def get_random_password(self) -> str:
        return common.crypto.generate_random_password(length=self['length'],
                                                      use_symbols=self['use_symbols'])


class Login(common.forms.ComfyForm):

    username = forms.CharField(max_length=models.MAX_CHAR_FIELD, required=True)
    master_password = forms.CharField(required=True)
