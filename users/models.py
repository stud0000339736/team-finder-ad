from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
import re
import uuid
import os


def user_avatar_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return os.path.join('avatars/', filename)


class UserManager(BaseUserManager):
    def create_user(
            self,
            name,
            surname,
            email,
            phone=None,
            github_url=None,
            avatar=None,
            password=None,
            about=None,
            **other_fields
    ):

        phone_re = re.compile(r'(^\+7\d{10}$)|(^8\d{10}$)')
        github_url_re = re.compile(r'^https://github.com/[\w-]+/?$')

        if phone and phone_re.match(phone) is None:
            raise ValueError('Неправильный номер телефона')

        if github_url and github_url_re.match(github_url) is None:
            raise ValueError('Неправильная ссылка на GitHub')

        if not email:
            raise ValueError("Нет почты")

        email = self.normalize_email(email)
        user = self.model(
            name=name,
            surname=surname,
            about=about,
            phone=phone,
            github_url=github_url,
            email=email,
            **other_fields)
        user.set_password(password)

        user.save(using=self._db)

        return user

    def create_superuser(
            self,
            name,
            surname,
            email,
            phone=None,
            github_url=None,
            avatar=None,
            password=None,
            about=None,
            **other_fields
    ):
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError('is_staff must be true')

        if other_fields.get('is_superuser') is not True:
            raise ValueError('is_superuser must be true')

        return self.create_user(
            name=name,
            surname=surname,
            email=email,
            about=about or '',
            phone=phone,
            github_url=github_url,
            avatar=avatar,
            password=password,
            **other_fields
        )


class User(AbstractUser):
    username = None
    name = models.CharField('Имя', max_length=124)
    surname = models.CharField('Фамилия', max_length=124)
    first_name = None
    last_name = None
    email = models.EmailField('Электронная почта', unique=True)
    about = models.CharField('Описание', blank=True, max_length=256, default='')
    phone = models.CharField('Номер телефона', max_length=12, blank=True, null=True)
    github_url = models.URLField('Ссылка на GitHub', blank=True, null=True)
    avatar = models.ImageField('Фото', upload_to=user_avatar_path, null=True, blank=True)
    favorites = models.ManyToManyField(
        'projects.Project',
        related_name='interested_users',
        blank=True,
        verbose_name='Проекты'
    )
    skill = models.ForeignKey(
        'users.Skill',
        related_name='users',
        blank=True,
        null=True,
        on_delete=models.CASCADE
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'surname']

    objects = UserManager()

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.name


class Skill(models.Model):
    name = models.CharField(max_length=124)

    class Meta:
        verbose_name = 'Навык'
        verbose_name_plural = 'Навыки'

    def __str__(self):
        return self.name
