from django import forms
from .models import CustomAbstractUser


class PasswordForm(forms.ModelForm):
    class Meta:
        model = CustomAbstractUser
        widgets = {
            "password": forms.PasswordInput(),
        }
