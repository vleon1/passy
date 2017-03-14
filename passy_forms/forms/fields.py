from django import forms

from passy.models import MAX_CHAR_FIELD
from passy.helpers.crypto import minimum_password_length, maximum_password_length, generate_random_password

from passy_forms.forms.widgets import TextInput, PasswordInput, NumberInput, CheckboxInput, TextPasswordInput


class CharField(forms.CharField):
    widget = TextInput

    def __init__(self, max_length=MAX_CHAR_FIELD, *args, **kwargs):
        super().__init__(max_length=max_length, *args, **kwargs)


class EmailField(forms.EmailField):
    widget = TextInput


class PasswordField(forms.CharField):
    widget = PasswordInput

    def __init__(self, min_length=minimum_password_length, max_length=maximum_password_length, *args, **kwargs):
        super().__init__(max_length=max_length, min_length=min_length, *args, **kwargs)


class TextPasswordField(PasswordField):
    widget = TextPasswordInput

    def __init__(self, initial=generate_random_password, *args, **kwargs):
        super().__init__(initial=initial, *args, **kwargs)


class IntegerField(forms.IntegerField):
    widget = NumberInput


class BooleanField(forms.BooleanField):
    widget = CheckboxInput

    def __init__(self, required=False, *args, **kwargs):
        """ It make no sense to default to required with checkboxes, since it means that we will by default only accept checked values.."""
        super().__init__(required=required, *args, **kwargs)

