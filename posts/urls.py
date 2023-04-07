from django.urls import path
from .views import *
from . import views
from django.conf.urls.static import static
from django.conf import settings

app_name = 'posts'
urlpatterns = [
    # path('home/', home, name='home'),
    # path('detail/<int:post_id>', detail, name='detail'),
    # path('new/', new, name='new'),
    # path('create/', create, name='create'),
    # path('update_page/<int:post_id>/', update_page, name='update_page'),
    # path('update/<int:post_id>/', update, name='update'),
    # path('delete/<int:post_id>/', delete, name='delete'),
    #
    # path('new_comment/<int:post_id>', new_comment, name='new_comment'),
    # path('create_comment/<int:post_id>', create_comment, name='create_comment'),
    # path('delete_comment/<int:comment_id>/', delete_comment, name='delete_comment'),
    path('', PostList.as_view()),
    path('<int:post_id>/', PostDetail.as_view()),
    path('comment/', CommentList.as_view()),
    path('comment/<int:comment_id>/', CommentDetail.as_view()),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)