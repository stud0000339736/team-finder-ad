from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
import re
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

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        if phone:
            phone_re = re.compile(r'(^\+7\d{10}$)|(^8\d{10}$)')
            if not phone_re.match(phone):
                raise forms.ValidationError('Неправильный номер телефона')
        return phone

    def clean_github_url(self):
        url = self.cleaned_data.get('github_url')
        if url:
            github_url_re = re.compile(r'^https://github.com/[\w-]+/?$')
            if not github_url_re.match(url):
                raise forms.ValidationError('Неправильная ссылка на GitHub')
        return url


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

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        if phone:
            phone_re = re.compile(r'(^\+7\d{10}$)|(^8\d{10}$)')
            if not phone_re.match(phone):
                raise forms.ValidationError('Неправильный номер телефона')
        return phone

    def clean_github_url(self):
        url = self.cleaned_data.get('github_url')
        if url:
            github_url_re = re.compile(r'^https://github.com/[\w-]+/?$')
            if not github_url_re.match(url):
                raise forms.ValidationError('Неправильная ссылка на GitHub')
        return url


class UserLoginForm(AuthenticationForm):
    username = forms.EmailField(label='Почта')
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)
