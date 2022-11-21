from django.db import models
from django.contrib.auth.models import (
    AbstractUser,
)
from django.utils.crypto import get_random_string
import uuid
import hashlib


class User(AbstractUser):
    """Model User от AbstractUser."""

    ROlE = (
        ('user', 'Пользователь'),
        ('moderator', 'Модератор'),
        ('admin', 'Администратор')
    )
    password = models.CharField(
        'Пароль',
        max_length=128,
        default=False
    )
    bio = models.TextField('Биография', blank=True)
    email = models.EmailField(
        'Электронная почта',
        max_length=254,
        unique=True
    )
    confirmation_code = models.CharField(
        'Код подтверждения',
        max_length=256,
        blank=True
    )
    role = models.CharField(
        'Роль',
        max_length=30,
        choices=ROlE,
        default='user'
    )

    class Meta:
        """Класс Meta."""

        ordering = ['-date_joined']
        constraints = [
            models.CheckConstraint(
                check=~models.Q(username='me'),
                name='not_me'
            )
        ]

    def __str__(self):
        """Возвращает username."""
        return self.username

    @property
    def is_admin(self):
        """."""
        return self.role == 'admin'

    @property
    def is_moderator(self):
        """."""
        return self.role == 'moderator'

    def make_confirmation_code(self):
        """Делаем confirmation_code."""
        return get_random_string()

    def hash_confirmation_code(self, confirmation_code):
        """Хэшируем confirmation_code."""
        salt = uuid.uuid4().hex
        confirmation_code = (hashlib.sha256(salt.encode() + confirmation_code.encode()).hexdigest() + ':' + salt)
        return (hashlib.sha256(salt.encode() + confirmation_code.encode()).hexdigest() + ':' + salt)

    def check_confirmation_code(self, hash_code, user_code):
        """Декодировка и проверка."""
        confirmation_code, salt = hash_code.split(':')
        return (
            confirmation_code == hashlib.sha256
            (salt.encode() + user_code.encode()).hexdigest()
        )
