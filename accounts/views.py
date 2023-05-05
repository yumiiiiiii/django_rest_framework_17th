
from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.contrib import auth
from .models import User, Friend

from rest_framework.response import Response
from rest_framework import status, viewsets
from .serializers import ProfileSerializer, SignUpSerializer, LoginSerializer, FriendSerializer
from rest_framework.views import APIView
# Create your views here.


class SignUpView(APIView):
    serializer_class = SignUpSerializer

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({'message': '회원가입 성공', 'data': serializer.data}, status=status.HTTP_201_CREATED)
        return Response({'message': '회원가입 실패', 'data': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            return Response({'message': "로그인 성공", 'data': serializer.validated_data}, status=status.HTTP_200_OK)
        return Response({'message': "로그인 실패", 'data': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class ProfileView(APIView):
    serializer_class = ProfileSerializer

    def get(self, request):
        user = request.user
        data = get_object_or_404(User, pk=user.id)

        serializer = self.serializer_class(data)

        return Response({'message': "프로필 조회 성공", 'data': serializer.validated_data}, status=status.HTTP_200_OK)

class FriendList(APIView):

    def get(self, request, format=None):
        user = self.request.user.profile
        friend = Friend.objects.filter(user=user)
        serializer = FriendSerializer(friend, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        user = self.request.user.profile
        serializer=FriendSerializer(data=request.data)
        if serializer.is_valid():
            if Friend.objects.filter(user=user, friend=serializer.validated_data['friend']):
                old_frined = Friend.objects.get(user=user, friend=serializer.validated_data['friend']) #validated_data로
                old_frined.delete()
            else:
                serializer.save(user=self.request.user.profile, friend=serializer.validated_data['friend'])
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class FriendViewSet(viewsets.ModelViewSet):
#     queryset=Friend.objects.all()
#     serializer_class=FriendSerializer
#
#     def perform_create(self, serializer):
#         serializer.save(user = self.request.user.profile)


#로그아웃 함수
class LogoutView(APIView):

    def post(self, request):
        response = Response({
            "message": "로그아웃 성공"
            }, status=status.HTTP_202_ACCEPTED)
        auth.logout(request)

        return response








