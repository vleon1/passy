from django.forms import widgets


class TextInput(widgets.TextInput):
    template_name = 'passy_forms/forms/widgets/text_input.html'


class PasswordInput(widgets.PasswordInput):
    template_name = 'passy_forms/forms/widgets/text_input.html'


class NumberInput(widgets.TextInput):
    input_type = 'text'
    template_name = 'passy_forms/forms/widgets/number_input.html'

    def __init__(self, attrs: dict=None):

        if attrs is None:
            attrs = {}

        attrs["pattern"] = r"^[0-9]+$"
        attrs["title"] = "numbers only"

        super().__init__(attrs=attrs)


class TextPasswordInput(widgets.TextInput):
    template_name = 'passy_forms/forms/widgets/password_input.html'


class CheckboxInput(widgets.CheckboxInput):
    template_name = 'passy_forms/forms/widgets/checkbox_input.html'
