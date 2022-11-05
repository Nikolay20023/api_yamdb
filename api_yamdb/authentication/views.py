from rest_framework.views import APIView
from .serializers import RegistrationSerializers
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.mail import send_mail
from users.models import User
import random
import string


class RegistrationClass(APIView):
    serializer_class = RegistrationSerializers
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            confirmation_code = int(
                "".join(random.choice(string.digits) for x in range(10))
            )
            send_mail(
                'confirmation_code',
                f'{confirmation_code}',
                'drom@mail.ru',
                serializer.data('email')
            )
            user = User.objects.create(**serializer.data)
            user.confirmation_code = confirmation_code


class AuthenticatedClass(APIView):
    serializer_class = RegistrationSerializers
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        confirmation_code = serializer.data.pop('confirmation_code', None)
        # if serializer.is_valid and confirmation_code:
