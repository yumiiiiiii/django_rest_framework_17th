import django_filters
from .models import *

class PostFilter(django_filters.filterset):
    class Meta:
        model = Post
        fields={
            'content':['icontains'],
        }