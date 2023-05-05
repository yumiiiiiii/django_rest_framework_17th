from django.urls import path, include
from .views import *
from rest_framework.routers import DefaultRouter

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

app_name = 'accounts'

router = DefaultRouter()

urlpatterns = [
    path('friend/', FriendList.as_view()),
    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('signup/', SignUpView.as_view()),

    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/token/', TokenRefreshView.as_view(), name='token_refresh'),
]