from django.conf import settings
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager,
)
from django.db import models

CHOICES_ROLE = [
    ('user', 'Пользователь'),
    ('moderator', 'Модератор'),
    ('admin', 'Админ'),
    ('superuser', 'Суперпользователь'),
]


class UserManager(BaseUserManager):
    """Чтобы определить кастомного пользователя определяем свой менеджер."""

    def create_user(
        self, username, bio, email=None, password=None, role='users',
    ):
        """Создаём обычного пользователя."""
        if username is None:
            raise TypeError('Пользователи должны быть с именем.')

        if email is None:
            raise TypeError('Пользователи должны быть с эл.почтой.')

        user = self.model(username=username, email=self.normalize_email(email))
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, username, email, password=None):
        """Создаём  супер пользователя."""
        if password is None:
            raise TypeError('Супер должен быть с паролем ')

        user = self.create_user(username, email, password)
        user.is_superusr = True
        user.is_staff = True
        user.save()

        return user


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(db_index=True, max_length=255)
    email = models.EmailField(
        db_index=True,
        unique=True,
        null=False,
        blank=False,
    )
    bio = models.TextField(
        'Биография',
        blank=True
    )
    confirmation_code = models.CharField(null=True, blank=False, max_length=16)
    role = models.CharField(
        max_length=16,
        choices=CHOICES_ROLE,
        default='user'
    )
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username
