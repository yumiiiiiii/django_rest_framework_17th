from django.urls import path
from .views import *
from . import views
from django.conf.urls.static import static
from django.conf import settings

app_name = 'posts'
urlpatterns = [
    path('home/', home, name='home'),
    path('detail/<int:post_id>', detail, name='detail'),
    # path('login/', login, name='login'),
    # path('logout/', logout, name='logout'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)