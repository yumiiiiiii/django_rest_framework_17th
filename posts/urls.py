from django.urls import path
from .views import *
from . import views
from django.conf.urls.static import static
from django.conf import settings

app_name = 'posts'
urlpatterns = [
    path('home/', home, name='home'),
    path('detail/<int:post_id>', detail, name='detail'),
    path('new/', new, name='new'),
    path('create/', create, name='create'),
    path('update_page/<int:post_id>/', update_page, name='update_page'),
    path('update/<int:post_id>/', update, name='update'),
    path('delete/<int:post_id>/', delete, name='delete'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)