from rest_framework import serializers
from users.models import User
from rest_framework.validators import UniqueTogetherValidator


class RegistrationSerializers(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    email = serializers.CharField(required=True)
    role = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'bio', 'role', 'confirmation_code')

    read_only_fields = ('role',)

    def validated_data(self, request):
        if request['username'] == 'me':
            raise serializers.ValidationError('username == me недопустимо.')
        return request
