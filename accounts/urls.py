from django.urls import path, include
from .views import *
from rest_framework.routers import DefaultRouter

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

app_name = 'accounts'

router = DefaultRouter()

# router.register('user', UserViewSet)
# router.register('profile', ProfileViewSet)
# router.register('friend', FriendViewSet)


urlpatterns = [
    # path('user/', UserList.as_view()),
    # path('user/<int:user_id>/', UserDetail.as_view()),
    # path('profile/', ProfileList.as_view()),
    # path('profile/<int:profile_id>/', ProfileDetail.as_view()),
    path('friend/', FriendList.as_view()),
    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('signup/', SignUpView.as_view()),
    # path('profile/', ProfileView.as_view()),
    # path('', include(router.urls)),

    # path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/token/', TokenRefreshView.as_view(), name='token_refresh'),
]