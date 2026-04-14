from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse

from core.constants import MAX_LENGTH_ABOUT, MAX_LENGTH_NAME, MAX_LENGTH_PHONE
from core.service import generate_avatar, user_avatar_path
from core.validators import validate_github_user_url, validate_phone
from users.managers import UserManager


class User(AbstractUser):
    username = None
    name = models.CharField('Имя', max_length=MAX_LENGTH_NAME)
    surname = models.CharField('Фамилия', max_length=MAX_LENGTH_NAME)
    first_name = None
    last_name = None
    email = models.EmailField('Электронная почта', unique=True)
    about = models.CharField('Описание', blank=True, max_length=MAX_LENGTH_ABOUT, default='')
    phone = models.CharField(
        'Номер телефона',
        max_length=MAX_LENGTH_PHONE,
        blank=True,
        null=True,
        validators=[validate_phone]
    )
    github_url = models.URLField(
        'Ссылка на GitHub',
        blank=True,
        null=True,
        validators=[validate_github_user_url]
    )
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

    def get_absolute_url(self):
        return reverse('users:profile', kwargs={'user_id': self.pk})

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)
        if is_new and not self.avatar:
            generate_avatar(self, self.name[0])
            super().save(update_fields=['avatar'])


class Skill(models.Model):
    name = models.CharField(max_length=MAX_LENGTH_NAME)

    class Meta:
        verbose_name = 'Навык'
        verbose_name_plural = 'Навыки'

    def __str__(self):
        return self.name
