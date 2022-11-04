from .models import User
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from rest_framework import filters
from django.core.mail import send_mail
from rest_framework.permissions import IsAdminUser


from .serializers import RegistrationSerializer, AdminSerializer


class UserSerializer(APIView):
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
    permission_classes = (IsAdminUser,)