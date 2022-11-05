from rest_framework import serializers
from users.models import User
from rest_framework.validators import UniqueTogetherValidator


class RegistrationSerializers(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('email', 'username', 'bio', 'role')

    read_only_fields = ('role',)

    def validated_data(self, data):
        if data['username'] == 'me':
            raise serializers.ValidationError('username == me недопустимо.')
        return data

