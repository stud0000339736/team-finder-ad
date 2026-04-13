from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from .models import User


class UserRegisterForm(UserCreationForm):
    password1 = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput
    )
    password2 = forms.CharField(
        label='Подтверждение пароля',
        widget=forms.PasswordInput
    )

    class Meta:
        model = User
        fields = (
            'name',
            'surname',
            'email',
            'phone',
            'github_url',
            'about',
            'avatar',
        )


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = (
            'name',
            'surname',
            'phone',
            'github_url',
            'about',
            'avatar',
        )
        widgets = {
            'avatar': forms.FileInput(attrs={'id': 'id_avatar', 'style': 'display:none;'}),
        }


class UserLoginForm(AuthenticationForm):
    username = forms.EmailField(label='Почта')
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)
