from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):

    def create_user(self, name, surname, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Нет Email")

        email = self.normalize_email(email)

        user = self.model(
            name=name,
            surname=surname,
            email=email,
            **extra_fields
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, name, surname, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('is_staff must be true')

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('is_superuser must be true')

        return self.create_user(
            name=name,
            surname=surname,
            email=email,
            password=password,
            **extra_fields
        )
