from django import forms
import re
from .models import Project


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ('name', 'description', 'github_url', 'status')
        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': 'Название проекта'
            }),
            'description': forms.Textarea(attrs={
                'placeholder': 'Описание проекта'
            }),
            'github_url': forms.URLInput(attrs={
                'placeholder': 'https://github.com/username/repo'
            }),
        }

    def clean_github_url(self):
        url = self.cleaned_data.get('github_url')
        if url:
            github_url_re = re.compile(r'^https://github.com/[\w-]+/[\w.-]+/?$')
            if not github_url_re.match(url):
                raise forms.ValidationError('Неправильная ссылка на GitHub')
        return url
