import random

from django.core.management.base import BaseCommand

from core.constants import STATUS_OPEN
from projects.models import Project
from users.models import User


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        for i in range(1, 20):
            base = f'testuser_{i}'
            email = f'{base}@test.com'

            if not User.objects.filter(email=email).exists():
                user = User.objects.create_user(
                    name=f'{base}_name',
                    surname=f'{base}_surname',
                    about=f'{base}_test_about_information',
                    email=email,
                    password='test',
                )

                for j in range(random.randint(1, 3)):
                    project = Project.objects.create(
                        name=f'test_project_{i}_{j}',
                        description=f'test_description_{i}_{j}',
                        owner=user,
                        status=STATUS_OPEN
                    )

                    project.participants.add(user)
