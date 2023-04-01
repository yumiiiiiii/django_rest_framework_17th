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
    image=models.ImageField(blank=True, null=True, upload_to="post_image")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.content} : {self.user}'
