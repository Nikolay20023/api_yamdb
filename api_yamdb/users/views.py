from rest_framework.views import APIView
from .serializers import (
    UserAuthSerializer,
    UserCreationSerializer,
    UserSerializers,
)
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from django.core.mail import send_mail
from .models import User
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status, filters
from rest_framework.permissions import IsAuthenticated
from .permissions import AdminOrSuperUSerOnly
from rest_framework.pagination import LimitOffsetPagination


class RegistrationClass(APIView):
    """Api класс для регистрации."""

    serializer_class = UserCreationSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        """POST запрос для регистрации."""
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = User.objects.create(**serializer.data)
            user.is_active = False
            confirmation_code = user.make_confirmation_code()
            send_mail(
                'welcome',
                f'{confirmation_code}',
                'EMAIL_HOST',
                [f'{user.email}', ]
            )
            user.confirmation_code = User.hash_confirmation_code(
                self,
                confirmation_code
            )
            user.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetTokenClass(APIView):
    """Класс для получения токена."""

    permission_classes = (AllowAny, )

    def post(self, request):
        """POST запрос на получение JWT токена."""
        serializer = UserAuthSerializer(data=request.data)
        if serializer.is_valid():
            return Response(
                data={'access': str(serializer.validated_data)},
                status=status.HTTP_200_OK
            )
        return Response(status=status.HTTP_400_BAD_REQUEST)


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
            serializer = UserSerializers(user)
            return Response(serializer.data)
        serializer = UserSerializers(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        if serializer.validated_data.get('role'):
            serializer.validated_data.pop('role')
        serializer.save()
        return Response(serializer.data)
