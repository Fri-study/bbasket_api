from django import forms
from .models import CustomAbstractBaseUser


class PasswordForm(forms.ModelForm):
    class Meta:
        model = CustomAbstractBaseUser
        widgets = {
            "password": forms.PasswordInput(),
        }
