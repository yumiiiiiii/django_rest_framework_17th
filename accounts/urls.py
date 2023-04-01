from django.urls import path
from .views import *
from . import views

app_name = 'accounts'
urlpatterns = [
    path('home/', home, name='home'),
    path('signup/', signup, name='signup'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
]