from django.db import models
# from django.contrib.auth.models import User
from accounts.models import Profile

# from accounts.models import Profile
# Create your models here.


class Post(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    content=models.TextField()
    is_anony=models.BooleanField(default=True)
    is_question=models.BooleanField(default=False)
    image=models.ImageField(blank=True, null=True, upload_to="post_image") #image 필드로 바꾸고 s3연결
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.content} : {self.user}'


class Comment(models.Model):
    post=models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    content = models.TextField()
    is_anony = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    re_comment = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f'{self.content} : {self.user}'
