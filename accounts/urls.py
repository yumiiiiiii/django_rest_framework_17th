from django.urls import path
from .views import *
from . import views

app_name = 'accounts'
urlpatterns = [
    # path('home/', home, name='home'),
    # path('signup/', signup, name='signup'),
    # path('login/', login, name='login'),
    # path('logout/', logout, name='logout'),
    #
    # path('friend/', friend, name='friend'),
    # path('new-friend/<int:profile_id>/', new_friend, name='new-friend'),
    path('profile/', ProfileList.as_view())
]