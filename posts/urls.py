from django.urls import path
from .views import *
from django.conf.urls.static import static
from django.conf import settings

app_name = 'posts'
urlpatterns = [

    path('', PostList.as_view()),
    path('<int:post_id>/', PostDetail.as_view()),
    path('comment/', CommentList.as_view()),
    path('comment/<int:comment_id>/', CommentDetail.as_view()),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)