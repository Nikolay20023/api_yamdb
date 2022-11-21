from rest_framework.views import APIView
from api.serializers import (
    UserAuthSerializer,
    UserCreationSerializer,
    UserSerializers,
)
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from django.core.mail import send_mail
from .models import User
from django.contrib.auth.tokens import default_token_generator
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status, filters
from rest_framework.permissions import IsAuthenticated
from api.permissions import AdminOrSuperUSerOnly
from rest_framework.pagination import LimitOffsetPagination
from django.shortcuts import get_object_or_404
from django.conf import settings
from rest_framework_simplejwt.tokens import AccessToken
from django.utils.crypto import get_random_string


class RegistrationClass(APIView):
    """Api класс для регистрации."""

    serializer_class = UserCreationSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        """POST запрос для регистрации."""
        serializer = UserCreationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.data['email']
        username = serializer.data['username']

        user, _ = User.objects.get_or_create(email=email, username=username)
        user.password = get_random_string()
        confirmation_code = default_token_generator.make_token(user)

        send_mail(
            'Код подтверждения',
            f'Ваш код подтверждения: {confirmation_code}',
            settings.DEFAULT_FROM_EMAIL,
            [email],
            fail_silently=False
        )

        return Response(serializer.data, status=status.HTTP_200_OK)


class GetTokenClass(APIView):
    """Класс для получения токена."""

    permission_classes = (AllowAny, )

    def post(self, request):
        """POST запрос на получение JWT токена."""
        serializer = UserAuthSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )
        username = serializer.data.get('username')
        confirmation_code = serializer.data.get('confirmation_code')
        user = get_object_or_404(User, username=username)
        if default_token_generator.check_token(user, confirmation_code):
            token = AccessToken.for_user(user)
            return Response(
                {token: str(token)}, status=status.HTTP_200_OK
            )
        return Response(
            {'confirmation_code': 'Неверный код подтверждения'},
            status=status.HTTP_400_BAD_REQUEST
        )


class AdminViewSet(viewsets.ModelViewSet):
    """Viewset для админа и суперпользователя."""

    serializer_class = UserSerializers
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated & AdminOrSuperUSerOnly,)
    pagination_class = LimitOffsetPagination
    filter_backends = [filters.SearchFilter, ]
    search_fields = ('username', )
    lookup_field = 'username'

    @action(
        detail=False,
        methods=['get', 'patch'],
        url_path='me',
        url_name='me',
        permission_classes=(IsAuthenticated, )
    )
    def me(self, request):
        """Запрос на me."""
        user = self.request.user
        if request.method == 'GET':
            serializer = self.get_serializer(user)
            return Response(serializer.data)
        serializer = UserSerializers(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save(role=user.role, partial=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
