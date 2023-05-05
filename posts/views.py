from .permissions import IsOwnerOrReadOnly
from .serializers import *

from rest_framework import viewsets, filters

# Create your views here.

class PostViewSet(viewsets.ModelViewSet):
    queryset=Post.objects.all()
    serializer_class=PostSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['content', 'user__nickname']

    permission_classes = [IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user = self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    queryset=Comment.objects.all()
    serializer_class=CommentSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


