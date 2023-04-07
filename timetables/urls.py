from django.urls import path
from .views import *


app_name = 'timetables'
urlpatterns = [
    path('', TimetableList.as_view()),
    path('<int:timetable_id>/', TimetableDetail.as_view()),
    path('subject/', SubjectList.as_view()),
    path('subject/<int:subject_id>/', SubjectDetail.as_view()),

]