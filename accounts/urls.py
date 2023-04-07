from django.urls import path
from .views import *
from . import views

app_name = 'accounts'
urlpatterns = [
    path('user/', UserList.as_view()),
    path('user/<int:user_id>/', UserDetail.as_view()),
    path('profile/', ProfileList.as_view()),
    path('profile/<int:profile_id>/', ProfileDetail.as_view()),
]