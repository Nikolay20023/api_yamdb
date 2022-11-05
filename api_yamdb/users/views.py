from .models import User
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status

from .serializers import (
    RegistrationSerializer,
    AdminSerializer,
    UserSerializer
)


class UserApi(APIView):
    permission_classes = (AllowAny,)
    serializer_class = RegistrationSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({
            'token': serializer.data.get('token', None),
        }, status=status.HTTP_201_CREATED)


class AdminViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = AdminSerializer


class UserInfo(APIView):

    def get(self, request):
        if request.user.is_authenticated:
            user = get_object_or_404(User, username=request.user.username)
            serializer = UserSerializer(user)
            return Response(serializer.data)
        return Response(
            'Вы не авторитизированы',
            status=status.HTTP_401_UNAUTHORIZED
        )

    def patch(self, request):
        if request.user.is_authenticated:
            user = get_object_or_404(User, username=request.user.username)
            serializer = UserSerializer(user, data=request.data)
            if serializer.is_valid:
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response(
            'Вы не авторитизированы',
            status=status.HTTP_401_UNAUTHORIZED
        )
