import json

from passy import models
from passy.helpers import crypto
from passy.helpers import typing

from passy_forms.forms.fields import CharField, EmailField, PasswordField, IntegerField, BooleanField, TextPasswordField
from passy_forms.forms.forms import Form


class StoredPassword(Form):

    site = CharField(label="Site or application name:")
    stored_password_text = TextPasswordField(label="New password:")

    @classmethod
    def from_request_and_instance(cls, request: typing.Request, instance: models.StoredPassword) -> "StoredPassword":

        request_data = json.loads(request.body) if request.body else dict()

        site = request_data.get("site") or instance.site
        stored_password_text = request_data.get("stored_password_text") or instance.get(master_password=request.session['master_password'])

        final_data = dict(site=site, stored_password_text=stored_password_text)

        return cls(data=final_data)

    def create_model(self, request: typing.Request) -> bool:

        instance = models.StoredPassword()

        return self.update_model(request, instance, check_for_existing_user=True)

    def update_model(self, request: typing.Request, instance: models.StoredPassword, check_for_existing_user: bool = False) -> bool:

        if not self.is_valid():
            return False

        instance.site = self.get_value('site')
        instance.owner = request.user

        instance.set(self.get_value('stored_password_text'), request.session['master_password'])

        if check_for_existing_user and models.StoredPassword.objects.filter(owner=request.user, site=instance.site).exists():
            self.add_error(field='site', error=f"This name {instance.site} is already used for another password")
            return False
        else:
            instance.save()

        return True


class GeneratedPasswordRequest(Form):

    length = IntegerField(initial=crypto.default_password_length)
    use_symbols = BooleanField(initial=True)

    def get_random_password(self) -> str:
        return crypto.generate_random_password(length=self.get_value('length'), use_symbols=self.get_value('use_symbols'))


class Login(Form):

    username = CharField(max_length=models.MAX_CHAR_FIELD, label="User Name:")
    master_password = PasswordField(label="Password:")


class Register(Form):

    email = EmailField(label="Email:", disabled=True)

    username = CharField(max_length=models.MAX_CHAR_FIELD, label="User Name:")

    password = PasswordField(label="Password:")
    repeated_password = PasswordField(label="Confirm password:")
