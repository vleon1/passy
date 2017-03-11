from django import forms

from passy_forms.forms.widgets import TextInput, PasswordInput, NumberInput, CheckboxInput, TextPasswordInput


class CharField(forms.CharField):
    widget = TextInput


class PasswordField(forms.CharField):
    widget = PasswordInput


class IntegerField(forms.IntegerField):
    widget = NumberInput


class BooleanField(forms.BooleanField):
    widget = CheckboxInput

    def __init__(self, required=False, *args, **kwargs):
        """ It make no sense to default to required with checkboxes, since it means that we will by default only accept checked values.."""
        super().__init__(required, *args, **kwargs)


class TextPasswordField(forms.CharField):
    widget = TextPasswordInput
