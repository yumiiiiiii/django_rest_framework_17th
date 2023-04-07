
from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.contrib import auth
from .models import Profile, Friend, User

from rest_framework.response import Response
from rest_framework import status, viewsets
from .serializers import ProfileSerializer, UserSerializer, FriendSerializer
from rest_framework.views import APIView
# Create your views here.

class UserList(APIView):
    def get(self, request, format=None):
        user=User.objects.all()
        serializer=UserSerializer(user, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer=UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDetail(APIView):
    def get_object(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            raise status.HTTP_404_NOT_FOUND

    def get(self, request, user_id, format=None):
        user=self.get_object(user_id)
        serializer=UserSerializer(user)
        return Response(serializer.data)

    def put(self, request, user_id, format=None):
        user = self.get_object(user_id)
        serializer=UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, user_id, format=None):
        user = self.get_object(user_id)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ProfileList(APIView):
    def get(self, request, format=None):
        profile=Profile.objects.all()
        serializer=ProfileSerializer(profile, many=True)
        return Response(serializer.data)

class ProfileDetail(APIView):

    def get_object(self, profile_id):
        try:
            return Profile.objects.get(pk=profile_id)
        except Profile.DoesNotExist:
            raise status.HTTP_404_NOT_FOUND

    def get(self, request, profile_id, format=None):
        profile=self.get_object(profile_id)
        serializer=ProfileSerializer(profile)
        return Response(serializer.data)

    def put(self, request, profile_id, format=None):
        profile = self.get_object(profile_id)
        serializer=ProfileSerializer(profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



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

#로그인 함수
class LoginView(APIView):
    serializer_class = UserSerializer
    def get(self, request):
        user = get_object_or_404(User, id=request.user.id)
        serializer = UserSerializer(user)
        return Response({'message': '현재 로그인된 유저 정보 조회 성공', 'data': serializer.data}, status=status.HTTP_200_OK)

    def post(self, request):
        user = auth.authenticate(request, username=request.POST['username'], password=request.POST['password'])
        # user = get_object_or_404(User, id=request.user.id)
        # serializer = UserSerializer(user)
        if user is not None:
            auth.login(request, user)
            serializer = UserSerializer(user)
            return Response({'data':serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)


#로그아웃 함수
class LogoutView(APIView):

    def post(self, request):
        response = Response({
            "message": "로그아웃 성공"
            }, status=status.HTTP_202_ACCEPTED)
        auth.logout(request)

        return response








