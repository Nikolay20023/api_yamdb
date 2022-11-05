from django.urls import path
from rest_framework_simplejwt import views as jwt_views
from .views import UserApi
from .views import UserInfo

urlpatterns = [
    path('v1/auth/signup/', UserApi.as_view()),
    path(
        'token/',
        jwt_views.TokenObtainPairView.as_view(),
        name='token_obtain_pair'
    ),
    path('v1/auth/token/', jwt_views.TokenRefreshView, name='token_refresh'),
    path('v1/users/me/', UserInfo.as_view(), name='user_info')
]
