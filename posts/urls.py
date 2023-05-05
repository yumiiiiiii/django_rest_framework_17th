from django.urls import path, include
from .views import *
from django.conf.urls.static import static
from django.conf import settings
from .views import *
from rest_framework.routers import DefaultRouter

app_name = 'posts'
router = DefaultRouter()

router.register('posts', PostViewSet) #comment list볼러면 설정해줘야함..

router.register('comments',CommentViewSet)

urlpatterns = [

    # path('', PostList.as_view()),
    # path('<int:post_id>/', PostDetail.as_view()),
    # path('comment/', CommentList.as_view()),
    # path('comment/<int:comment_id>/', CommentDetail.as_view()),

    path('', include(router.urls)),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)