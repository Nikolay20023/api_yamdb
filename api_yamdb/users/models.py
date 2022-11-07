from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager,
)
from django.db import models
from django.utils.crypto import get_random_string
import uuid
import hashlib

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

    def create_admin(self, username, bio, role, email, password=None):
        """Создаём  супер пользователя."""
        if password is None:
            raise TypeError('Админ должен быть с паролем ')

        user = self.create_user(username, email, password, bio, role)
        user.is_staff = True
        user.is_admin = True
        user.save()
        return user

    def create_moderator(
        self, username, bio, email, role='moderator', password=None,
    ):
        if password is None:
            raise TypeError('Модератор должен быть с паролем ')
        user = self.create_user(username, email, password, bio, role)
        user.is_moderator = True
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Чтобы определить кастомного пользователя определяем свой менеджер."""

    username = models.CharField(
        db_index=True,
        max_length=255,
        null=False,
        blank=False
    )
    email = models.EmailField(
        db_index=True,
        unique=True,
        null=False,
        blank=False,
    )
    bio = models.TextField(
        blank=True
    )
    confirmation_code = models.CharField(null=True, blank=False, max_length=16)
    role = models.CharField(
        max_length=16,
        choices=CHOICES_ROLE,
        default='user'
    )
    is_active = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def make_confirmation_code(self):
        return  get_random_string()

    def hash_confirmation_code(self, confirmation_code):
        salt = uuid.uuid4().hex
        return (hashlib.sha256(salt.encode() + confirmation_code.encode()).hexdigest() + ':' + salt)

    def check_confirmation_code(self, hash_code, user_code):
        confirmation_code, salt = hash_code.split(':')
        return (
            confirmation_code == hashlib.sha256
            (salt.encode() + user_code.encode()).hexdigest()
        )

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    def __str__(self):
        """Чтобы определить кастомного пользователя определяем свой ."""
        return self.username

    def get_full_name(self):
        """Чтобы определить кастомного пользователя определяем свой ."""
        return self.username

    def get_short_name(self):
        """Чтобы определить кастомного пользователя определяем свой ."""
        return self.username
