from django.db import models


STATUS = [
    ('open', 'Открыт'),
    ('closed', 'Закрыт')
]


class Project(models.Model):
    name = models.CharField('Название', max_length=200)
    description = models.TextField('Описание', blank=True)
    owner = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        related_name='owned_projects',
        verbose_name='Владелец'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    github_url = models.URLField('Ссылка на GitHub', blank=True)
    status = models.CharField('Статус', max_length=6, choices=STATUS, default='open')
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

    def __str__(self):
        return self.name


class Skill(models.Model):
    name = models.CharField(max_length=124)

    class Meta:
        verbose_name = 'Навык'
        verbose_name_plural = 'Навыки'

    def __str__(self):
        return self.name
