from rest_framework import serializers
from .models import *


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source = 'user.nickname')
    class Meta:
        model=Comment
        fields=['id','user','post','content','is_anony','created_at','updated_at','re_comment']

class PostSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.nickname')
    comment = CommentSerializer(many=True, source='comments', read_only=True) #source=model의 related_name 명시해야 보임

    class Meta:
        model = Post
        fields = ['id', 'user','content','is_anony','is_question','image','created_at', 'updated_at','comment']