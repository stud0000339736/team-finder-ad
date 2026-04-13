from django.db import models
from django.urls import reverse

from core.constants import (MAX_LENGTH_NAME, MAX_LENGTH_STATUS, STATUS_CLOSED,
                            STATUS_OPEN)
from core.validators import validate_github_project_url

STATUS = [
    (STATUS_OPEN, 'Открыт'),
    (STATUS_CLOSED, 'Закрыт')
]


class Project(models.Model):
    name = models.CharField('Название', max_length=MAX_LENGTH_NAME)
    description = models.TextField('Описание', blank=True)
    owner = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        related_name='owned_projects',
        verbose_name='Владелец'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    github_url = models.URLField(
        'Ссылка на GitHub',
        blank=True,
        validators=[validate_github_project_url]
    )
    status = models.CharField(
        'Статус',
        max_length=MAX_LENGTH_STATUS,
        choices=STATUS,
        default=STATUS_OPEN
    )
    participants = models.ManyToManyField(
        'users.User',
        blank=True,
        related_name='participated_projects',
        verbose_name='Участники'
    )
    skill = models.ForeignKey(
        'projects.Skill',
        blank=True,
        null=True,
        related_name='projects',
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = 'Проект'
        verbose_name_plural = 'Проекты'
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('projects:project_detail', kwargs={'project_id': self.pk})


class Skill(models.Model):
    name = models.CharField(max_length=MAX_LENGTH_NAME)

    class Meta:
        verbose_name = 'Навык'
        verbose_name_plural = 'Навыки'

    def __str__(self):
        return self.name
