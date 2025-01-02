from django import forms

from mailing.models import Client, Mailing


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name not in ["clients", "user", "is_active"]:
                field.widget.attrs["class"] = "form-control"


class MailingForm(StyleFormMixin, forms.ModelForm):
    clients = forms.ModelMultipleChoiceField(
        queryset=Client.objects.none(),  # Изначально пустой queryset
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = Mailing
        exclude = ["user", "is_active"]

    def __init__(self, *args, user=None, **kwargs):  # Добавляем user как аргумент
        super().__init__(*args, **kwargs)
        if user is not None:
            # Фильтруем клиентов по владельцу
            self.fields["clients"].queryset = Client.objects.filter(owner=user)

    def clean_day(self):
        cleaned_data = self.cleaned_data.get("day")
        if cleaned_data is None or not (1 <= cleaned_data <= 31):
            raise forms.ValidationError("Число должно быть от 1 до 31")
        return cleaned_data


class ClientForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Client
        fields = ["email", "full_name", "comment"]
