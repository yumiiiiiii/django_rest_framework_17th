from django.urls import path,include
from .views import *
from rest_framework.routers import DefaultRouter


app_name = 'timetables'
router = DefaultRouter()

router.register('timetable', TimetableViewSet) #comment list볼러면 설정해줘야함..

router.register('subject', SubjectViewSet)
urlpatterns = [
    # path('', TimetableList.as_view()),
    # path('<int:timetable_id>/', TimetableDetail.as_view()),
    # path('subject/', SubjectList.as_view()),
    # path('subject/<int:subject_id>/', SubjectDetail.as_view()),

    path('', include(router.urls)),

]