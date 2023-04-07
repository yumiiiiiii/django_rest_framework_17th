from django.shortcuts import render, get_object_or_404, redirect

from .models import *
from rest_framework.response import Response
from rest_framework import status
from .serializers import *
from rest_framework.views import APIView
# Create your views here.


class TimetableList(APIView):
    def get(self, request, format=None):
        timetable=Timetable.objects.all()
        serializer=TimetableSerializer(timetable, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer=TimetableSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=self.request.user.profile)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TimetableDetail(APIView):

    def get_object(self, timetable_id):
        try:
            return Timetable.objects.get(pk=timetable_id)
        except Timetable.DoesNotExist:
            raise status.HTTP_404_NOT_FOUND

    def get(self, request, timetable_id, format=None):
        timetable=self.get_object(timetable_id)
        serializer=TimetableSerializer(timetable)
        return Response(serializer.data)

    def put(self, request, timetable_id, format=None):
        timetalble = self.get_object(timetable_id)
        serializer=TimetableSerializer(timetalble, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, timetable_id, format=None):
        timetable = self.get_object(timetable_id)
        timetable.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# 여기부터 과목
class SubjectList(APIView):
    def get(self, request, format=None):
        subject=Subject.objects.all()
        serializer=SubjectSerializer(subject, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer=SubjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SubjectDetail(APIView):

    def get_object(self, subject_id):
        try:
            return Subject.objects.get(pk=subject_id)
        except Subject.DoesNotExist:
            raise status.HTTP_404_NOT_FOUND

    def get(self, request, subject_id, format=None):
        subject=self.get_object(subject_id)
        serializer=SubjectSerializer(subject)
        return Response(serializer.data)

    def put(self, request, subject_id, format=None):
        subject = self.get_object(subject_id)
        serializer=SubjectSerializer(subject, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, subject_id, format=None):
        subject = self.get_object(subject_id)
        subject.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
