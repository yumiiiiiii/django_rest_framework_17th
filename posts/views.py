from .models import *
from rest_framework.response import Response
from rest_framework import status
from .serializers import *
from rest_framework.views import APIView

from rest_framework import viewsets
# Create your views here.


# class PostList(APIView):
#     def get(self, request, format=None):
#         post=Post.objects.all()
#         serializer=PostSerializer(post, many=True)
#         return Response(serializer.data)
#
#     def post(self, request, format=None):
#         serializer=PostSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save(user=self.request.user.profile)
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
# class PostDetail(APIView):
#
#     def get_object(self, post_id):
#         try:
#             return Post.objects.get(pk=post_id)
#         except Post.DoesNotExist:
#             raise status.HTTP_404_NOT_FOUND
#
#     def get(self, request, post_id, format=None):
#         post=self.get_object(post_id)
#         serializer=PostSerializer(post)
#         return Response(serializer.data)
#
#     def put(self, request, post_id, format=None):
#         post = self.get_object(post_id)
#         serializer=PostSerializer(post, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     def delete(self, request, post_id, format=None):
#         post = self.get_object(post_id)
#         post.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
#
#
# # 여기부터 댓글 함수
# class CommentList(APIView):
#     def get(self, request, format=None):
#         comment=Comment.objects.all()
#         serializer=CommentSerializer(comment, many=True)
#         return Response(serializer.data)
#
#     def post(self, request, format=None):
#         serializer=CommentSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save(user=self.request.user.profile)
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
# class CommentDetail(APIView):
#
#     def get_object(self, comment_id):
#         try:
#             return Comment.objects.get(pk=comment_id)
#         except Comment.DoesNotExist:
#             raise status.HTTP_404_NOT_FOUND
#
#     def get(self, request, comment_id, format=None):
#         comment=self.get_object(comment_id)
#         serializer=CommentSerializer(comment)
#         return Response(serializer.data)
#
#     def put(self, request, comment_id, format=None):
#         comment = self.get_object(comment_id)
#         serializer=CommentSerializer(comment, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     def delete(self, request, comment_id, format=None):
#         comment = self.get_object(comment_id)
#         comment.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

class PostViewSet(viewsets.ModelViewSet):
    queryset=Post.objects.all()
    serializer_class=PostSerializer

    def perform_create(self, serializer):
        serializer.save(user = self.request.user.profile)


class CommentViewSet(viewsets.ModelViewSet):
    queryset=Comment.objects.all()
    serializer_class=CommentSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user.profile)

