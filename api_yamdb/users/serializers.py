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
        fields = ('username', 'email', 'password')

    def create(self, validated_data):
        User.objects.create_user(**validated_data)


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'password', 'email', 'token')

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
        paswword = validated_data.pop('password', None)
        email = validated_data.pop('email', None)
        instance = self.Meta.model(**validated_data)
        if (paswword is not None) and(email is not None):
            instance.set_password(paswword)
            instance.save()
            return instance