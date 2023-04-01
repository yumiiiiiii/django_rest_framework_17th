from django.db import models
from accounts.models import Profile

WEEK_CHOICES=[('Monday', 'Monday'), ('Tuesday', 'Tuesday'),
              ('Wednesday', 'Wednesday'), ('Thursday', 'Thursday'), ('Friday', 'Friday'),
              ('Saturday', 'Saturday'), ('Sunday', 'Sunday')]


class Timetable(models.Model):
    title=models.CharField(max_length=64)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title}"

class Subject(models.Model):
    timetable = models.ForeignKey(Timetable, on_delete=models.CASCADE, related_name='subjects')
    name = models.CharField(max_length=255)
    teacher = models.CharField(max_length=255)
    day=models.CharField(choices=WEEK_CHOICES, max_length=32)
    start_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)
    place=models.CharField(max_length=32, null=True, blank=True)

    def __str__(self):
        return f"{self.name} : {self.teacher}"

