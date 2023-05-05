from rest_framework.permissions import IsAuthenticated
from .serializers import *

# Create your views here.
from rest_framework import viewsets


class TimetableViewSet(viewsets.ModelViewSet):
    queryset=Timetable.objects.all()
    serializer_class=TimetableSerializer

    permission_classes = [IsAuthenticated, ]

    def perform_create(self, serializer):
        serializer.save(user = self.request.user)


class SubjectViewSet(viewsets.ModelViewSet):
    queryset=Subject.objects.all()
    serializer_class=SubjectSerializer

    def perform_create(self, serializer):
        serializer.save()
