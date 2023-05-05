from django.urls import path,include
from .views import *
from rest_framework.routers import DefaultRouter


app_name = 'timetables'
router = DefaultRouter()

router.register('timetables', TimetableViewSet) #comment list볼러면 설정해줘야함..

router.register('subjects', SubjectViewSet)
urlpatterns = [
    path('', include(router.urls)),

]