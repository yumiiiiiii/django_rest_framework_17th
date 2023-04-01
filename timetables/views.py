from django.shortcuts import render, get_object_or_404, redirect

import timetables.models
from .models import *
# Create your views here.

def home(request):
    timetables=Timetable.objects
    return render(request, 'timetables/home.html', {'timetables':timetables})

def detail(request, timetable_id):
    timetable_detail=get_object_or_404(Timetable, pk=timetable_id)
    return render(request, 'timetables/detail.html', {'timetable':timetable_detail})

def new(request):
    return render(request, 'timetables/new.html')

def create(request):
    me=request.user.profile
    if request.method == "POST":
        new_timetable=Timetable()
        new_timetable.title=request.POST['title']
        new_timetable.user = me
        new_timetable.save()
        return redirect('timetables:home')
    return render(request, 'timetables:home')

#과목 추가
def new_subject(request, timetable_id):
    timetable = get_object_or_404(Timetable, pk=timetable_id)
    return render(request, 'timetables/new_subject.html', {'timetable':timetable})


def create_subject(request, timetable_id):
    timetable = get_object_or_404(Timetable, pk=timetable_id)
    if request.method == "POST":
        new_subject=Subject()
        new_subject.timetable=timetable
        new_subject.name=request.POST['name']
        new_subject.teacher = request.POST['teacher']
        new_subject.day=request.POST['day']
        new_subject.start_time=request.POST.get('start_time')
        new_subject.end_time=request.POST.get('end_time')
        new_subject.save()
        return redirect('timetables:detail', timetable_id)
    return render(request, 'posts:home')