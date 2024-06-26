from typing import Any

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.forms.widgets import PasswordInput, TextInput

User = get_user_model()


class UserCreateForm(UserCreationForm):
    """Класс формы регистрации пользователя"""
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def ___init__(self, *args: Any, **kwargs: Any) -> None:
        super(UserCreateForm, self).__init__(*args, **kwargs)
        self.fields['email'].label = 'Your Email Address'
        self.fields['email'].required = True
        self.fields['username'].help_text = 'Your Username'
        self.fields['password1'].help_text = 'Your Password'

    def clean_email(self) -> str:
        email = self.cleaned_data['email'].lower()
        if User.objects.filter(email=email).exists() and len(email) > 254:
            raise forms.ValidationError(
                'User with this email already exists or too long'
            )
        return email
