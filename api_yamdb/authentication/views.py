from rest_framework.views import APIView
from .serializers import RegistrationSerializers
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.mail import send_mail
from users.models import User
from rest_framework.response import Response


def get_token(self, user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': refresh,
        'access': str(refresh.access_token)
    }

class RegistrationClass(APIView):
    serializer_class = RegistrationSerializers
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = User.objects.create(**serializer.data)
            user.is_active = False
            confirmation_code = user.make_confirmation_code()
            send_mail(
                'welcome',
                f'{confirmation_code}',
                user.email,
                ['EMAIL_HOST', ]
            )
            user.confirmation_code = User.hash_confirmation_code(self, confirmation_code)
            user.save()
            return Response(serializer.data)

class AuthenticatedClass(APIView):
    serializer_class = RegistrationSerializers
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        user = User.objects.filter(username=request.data['username'])
        if User.check_confirmation_code(user.confirmation_code, serializer.data['confirmation_code']):
            user.is_active = True
            user.save()
            get_token(self, user)
