from django.urls import path
from rest_framework_simplejwt import views as jwt_views
from .views import UserSerializer
from . import views

urlpatterns = [
    path('users/', UserSerializer.as_view()),
    path('token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', jwt_views.TokenRefreshView, name='token_refresh'),
    # path('user/create/', views.create_user, name='create_user')
]
