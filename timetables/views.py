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
        comment=Subject.objects.all()
        serializer=SubjectSerializer(comment, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer=SubjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=self.request.user.profile)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CommentDetail(APIView):

    def get_object(self, comment_id):
        try:
            return Comment.objects.get(pk=comment_id)
        except Comment.DoesNotExist:
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

# def home(request):
#     timetables=Timetable.objects
#     return render(request, 'timetables/home.html', {'timetables':timetables})
#
# def detail(request, timetable_id):
#     timetable_detail=get_object_or_404(Timetable, pk=timetable_id)
#     return render(request, 'timetables/detail.html', {'timetable':timetable_detail})
#
# def new(request):
#     return render(request, 'timetables/new.html')
#
# def create(request):
#     me=request.user.profile
#     if request.method == "POST":
#         new_timetable=Timetable()
#         new_timetable.title=request.POST['title']
#         new_timetable.user = me
#         new_timetable.save()
#         return redirect('timetables:home')
#     return render(request, 'timetables:home')
#
# #과목 추가
# def new_subject(request, timetable_id):
#     timetable = get_object_or_404(Timetable, pk=timetable_id)
#     return render(request, 'timetables/new_subject.html', {'timetable':timetable})
#
#
# def create_subject(request, timetable_id):
#     timetable = get_object_or_404(Timetable, pk=timetable_id)
#     if request.method == "POST":
#         new_subject=Subject()
#         new_subject.timetable=timetable
#         new_subject.name=request.POST['name']
#         new_subject.teacher = request.POST['teacher']
#         new_subject.day=request.POST['day']
#         new_subject.start_time=request.POST.get('start_time')
#         new_subject.end_time=request.POST.get('end_time')
#         new_subject.save()
#         return redirect('timetables:detail', timetable_id)
#     return render(request, 'posts:home')