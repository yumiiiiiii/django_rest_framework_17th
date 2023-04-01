from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Comment
from accounts.models import Profile
# Create your views here.

def home(request):
    posts=Post.objects
    return render(request, 'posts/home.html', {'posts':posts})


def detail(request, post_id):
    posts_detail=get_object_or_404(Post, pk=post_id)
    return render(request, 'posts/detail.html', {'post':posts_detail})


def new(request):
    return render(request, 'posts/new.html')


def create(request):
    me=request.user.profile
    if request.method == "POST":
        new_post=Post()
        new_post.content=request.POST['content']
        new_post.user = me
        if len(request.POST.getlist('is_anony')) == 0:
            new_post.is_anony = False
        else:
            new_post.is_anony = True
        if len(request.POST.getlist('is_question')) == 0:
            new_post.is_question = False
        else:
            new_post.is_question= True
        new_post.save()
        return redirect('posts:home')
    return render(request, 'posts:home')

def delete(request, post_id):
    post_delete=get_object_or_404(Post, pk=post_id)
    post_delete.delete()
    return redirect('posts:home')


def update_page(request, post_id):
    post_update=get_object_or_404(Post, pk=post_id)
    return render(request, 'posts/update.html', {'post':post_update})


def update(request, post_id):
    post_update = get_object_or_404(Post, pk=post_id)
    post_update.content = request.POST['content']
    if len(request.POST.getlist('is_anony')) == 0:
        post_update.is_anony = False
    else:
        post_update.is_anony = True
    if len(request.POST.getlist('is_question')) == 0:
        post_update.is_question = False
    else:
        post_update.is_question = True
    post_update.save()
    return redirect('posts:home')



#여기부터 댓글 함수
def new_comment(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    return render(request, 'posts/new_comment.html', {'post':post})


def create_comment(request, post_id):
    me=request.user.profile
    post=get_object_or_404(Post, pk=post_id)
    if request.method == "POST":
        new_comment=Comment()
        new_comment.post=post
        new_comment.content=request.POST['content']
        new_comment.user = me
        if len(request.POST.getlist('is_anony')) == 0:
            new_comment.is_anony = False
        else:
            new_comment.save()
        return redirect('posts:detail', post_id)
    return render(request, 'posts:home')


def delete_comment(request, comment_id):
    comment_delete=get_object_or_404(Comment, pk=comment_id)
    comment_delete.delete()
    return redirect('posts:home')

