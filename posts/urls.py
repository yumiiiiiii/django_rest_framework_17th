from django.urls import path
from .views import *
from . import views
from django.conf.urls.static import static
from django.conf import settings

app_name = 'posts'
urlpatterns = [
    # path('home/', home, name='home'),
    # path('signup/', signup, name='signup'),
    # path('login/', login, name='login'),
    # path('logout/', logout, name='logout'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)