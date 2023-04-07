from .models import *
from rest_framework.response import Response
from rest_framework import status
from .serializers import *
from rest_framework.views import APIView
# Create your views here.

# def home(request):
#     posts=Post.objects
#     return render(request, 'posts/home.html', {'posts':posts})
#
#
# def detail(request, post_id):
#     posts_detail=get_object_or_404(Post, pk=post_id)
#     return render(request, 'posts/detail.html', {'post':posts_detail})
#
#
# def new(request):
#     return render(request, 'posts/new.html')
#
#
# def create(request):
#     me=request.user.profile
#     if request.method == "POST":
#         new_post=Post()
#         new_post.content=request.POST['content']
#         new_post.user = me
#         if len(request.POST.getlist('is_anony')) == 0:
#             new_post.is_anony = False
#         else:
#             new_post.is_anony = True
#         if len(request.POST.getlist('is_question')) == 0:
#             new_post.is_question = False
#         else:
#             new_post.is_question= True
#         new_post.image=request.FILES['image']
#         new_post.save()
#         return redirect('posts:home')
#     return render(request, 'posts:home')
#
# def delete(request, post_id):
#     post_delete=get_object_or_404(Post, pk=post_id)
#     post_delete.delete()
#     return redirect('posts:home')
#
#
# def update_page(request, post_id):
#     post_update=get_object_or_404(Post, pk=post_id)
#     return render(request, 'posts/update.html', {'post':post_update})
#
#
# def update(request, post_id):
#     post_update = get_object_or_404(Post, pk=post_id)
#     post_update.content = request.POST['content']
#     if len(request.POST.getlist('is_anony')) == 0:
#         post_update.is_anony = False
#     else:
#         post_update.is_anony = True
#     if len(request.POST.getlist('is_question')) == 0:
#         post_update.is_question = False
#     else:
#         post_update.is_question = True
#     post_update.save()
#     return redirect('posts:home')
#
#
#
# #여기부터 댓글 함수
# def new_comment(request, post_id):
#     post = get_object_or_404(Post, pk=post_id)
#     return render(request, 'posts/new_comment.html', {'post':post})
#
#
# def create_comment(request, post_id):
#     me=request.user.profile
#     post=get_object_or_404(Post, pk=post_id)
#     if request.method == "POST":
#         new_comment=Comment()
#         new_comment.post=post
#         new_comment.content=request.POST['content']
#         new_comment.user = me
#         if len(request.POST.getlist('is_anony')) == 0:
#             new_comment.is_anony = False
#         else:
#             new_comment.save()
#         return redirect('posts:detail', post_id)
#     return render(request, 'posts:home')
#
#
# def delete_comment(request, comment_id):
#     comment_delete=get_object_or_404(Comment, pk=comment_id)
#     comment_delete.delete()
#     return redirect('posts:home')

class PostList(APIView):
    def get(self, request, format=None):
        post=Post.objects.all()
        serializer=PostSerializer(post, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer=PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=self.request.user.profile)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PostDetail(APIView):

    def get_object(self, post_id):
        try:
            return Post.objects.get(pk=post_id)
        except Post.DoesNotExist:
            raise status.HTTP_404_NOT_FOUND

    def get(self, request, post_id, format=None):
        post=self.get_object(post_id)
        serializer=PostSerializer(post)
        return Response(serializer.data)

    def put(self, request, post_id, format=None):
        post = self.get_object(post_id)
        serializer=PostSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, post_id, format=None):
        post = self.get_object(post_id)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# 여기부터 댓글 함수
class CommentList(APIView):
    def get(self, request, format=None):
        comment=Comment.objects.all()
        serializer=PostSerializer(comment, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer=CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=self.request.user.profile)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CommentDetail(APIView):

    def get_object(self, comment_id):
        try:
            return Comment.objects.get(pk=comment_id)
        except Coment.DoesNotExist:
            raise status.HTTP_404_NOT_FOUND

    def get(self, request, comment_id, format=None):
        comment=self.get_object(comment_id)
        serializer=CommentSerializer(comment)
        return Response(serializer.data)

    def put(self, request, comment_id, format=None):
        comment = self.get_object(comment_id)
        serializer=CommentSerializer(comment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, comment_id, format=None):
        comment = self.get_object(comment_id)
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
