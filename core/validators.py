from django.core.exceptions import ValidationError

from core.constants import (GITHUB_PROJECT_URL_REGEX, GITHUB_USER_REGEX,
                            PHONE_REGEX)


def validate_github_project_url(value):
    if value and not GITHUB_PROJECT_URL_REGEX.match(value):
        raise ValidationError('Неправильная ссылка на GitHub')


def validate_phone(value):
    if value and not PHONE_REGEX.match(value):
        raise ValidationError('Неправильный номер телефона')


def validate_github_user_url(value):
    if value and not GITHUB_USER_REGEX.match(value):
        raise ValidationError('Неправильная ссылка на GitHub')
