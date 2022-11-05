from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User


class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'bio', 'role')

    def create(self, validated_data):
        User.objects.create_user(**validated_data)


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'password', 'email', 'bio', 'role')

    token = serializers.SerializerMethodField()
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )

    def get_token(self, user):
        refresh = RefreshToken.for_user(user)
        return {
            'refresh': refresh,
            'access': str(refresh.access_token)
        }

    def create(self, validated_data):
        email = validated_data.pop('email', None)
        instance = self.Meta.model(**validated_data)
        if  email is not None:
            instance.save()
            return instance


class AdminSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'password',
            'bio',
            'role'
        )
        read_only_fields = ('role', )
