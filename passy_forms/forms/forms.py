from django.forms import forms


class Form(forms.Form):

    def get_value(self, name):

        self.is_valid()  # making sure we tried to clean the data before accessing it

        if self.is_bound and name in self.cleaned_data:
            return self.cleaned_data[name]

        field = self[name]

        return field.value() or ""

    def to_dict(self):
        return {name: self.get_value(name) for name in self.fields}
