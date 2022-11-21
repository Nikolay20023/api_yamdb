from rest_framework import serializers
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model

User = get_user_model()


class UserCreationSerializer(serializers.ModelSerializer):
    """Сериализация для регистрации."""

    username = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)

    class Meta:
        """Класс Meta."""

        model = User
        fields = ('username', 'email')

    def validate_email(self, value):
        """Валидация email."""
        email = value.lower()
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                f'Такой пользователь с указаннной {email} сущ.'
            )
        return value

    def validate_username(sefl, value):
        """Валидация username."""
        username = value.lower()
        if username == 'me':
            raise serializers.ValidationError(
                'Пользователь с me недоступен.'
            )
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError(
                f'Такой пользователь с указаннной {username} сущ.'
            )
        return value


class UserAuthSerializer(serializers.Serializer):
    """Скриализация для аутенфикации по токену."""

    username = serializers.CharField(max_length=150)
    confirmation_code = serializers.CharField(max_length=256)

    def validate(self, data):
        """Валидация confirmation_code."""
        user = get_object_or_404(User, username=data['username'])
        if user.confirmation_code != data['confirmation_code']:
            raise serializers.ValidationError('Неверный код подтверждения')
        return RefreshToken.for_user(user).access_token


class UserSerializers(serializers.ModelSerializer):
    """Скриализация для пользователей."""

    class Meta:
        """Класс Meta."""

        model = User
        fields = (
            'first_name',
            'last_name',
            'username',
            'bio',
            'role',
            'email'
        )
