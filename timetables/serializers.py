from rest_framework import serializers
from .models import *


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model=Subject
        fields=['id','timetable','name','teacher','day','start_time','end_time','place']


class TimetableSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.nickname')
    subject=SubjectSerializer(source='subjects', many=True, read_only=True)

    class Meta:
        model = Timetable
        fields = ['id', 'user','title','created_at', 'updated_at', 'subject']