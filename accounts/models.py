from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator


class User(AbstractUser):
    nickname = models.TextField(max_length=10, unique=True)
    university = models.TextField(max_length=16)
    enter_year = models.IntegerField(validators=[MinValueValidator(2000), MaxValueValidator(2030)], blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.username}'

class Friend(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friends')
    friend = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.nickname}"