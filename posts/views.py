from django.shortcuts import render, get_object_or_404
from .models import Post
# Create your views here.

def home(request):
    posts=Post.objects
    return render(request, 'posts/home.html', {'posts':posts})


def detail(request, post_id):
    posts_detail=get_object_or_404(Post, pk=post_id)
    return render(request, 'posts/detail.html', {'post':posts_detail})

