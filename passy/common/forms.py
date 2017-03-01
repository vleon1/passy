from django.forms import forms


class ComfyForm(forms.Form):
    """
    A form that is treated in a way more similar to how models work.
    """

    def __getitem__(self, name):
        self.is_valid()  # making sure we tried to clean the data before accessing it

        if self.is_bound and name in self.cleaned_data:
            return self.cleaned_data[name]

        field = self._parent_getitem(name)

        return field.value() or ""

    def to_dict(self):
        return {name: self[name] for name in self.fields}

    # some function fixed to work directly with parent methods to avoid braking their behaviour

    def _parent_getitem(self, name):
        return super().__getitem__(name)

    def _parent_iter(self):
        for name in self.fields:
            yield self._parent_getitem(name)

    def hidden_fields(self):
        return [field for field in self._parent_iter() if field.is_hidden]

    def visible_fields(self):
        return [field for field in self._parent_iter() if not field.is_hidden]
