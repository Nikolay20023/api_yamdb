from django.urls import path, include
from . views import (
    RegistrationClass,
    GetTokenClass,
    AdminViewSet,
)
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'users', AdminViewSet)

urlpatterns = [
    path(r'v1/auth/signup/', RegistrationClass.as_view()),
    path(r'v1/auth/token/', GetTokenClass.as_view()),
    path('v1/', include(router.urls)),
]
