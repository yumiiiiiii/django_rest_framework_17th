from django.contrib.auth import authenticate
from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.contrib import auth
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import User, Friend

from rest_framework.response import Response
from rest_framework import status, viewsets
from .serializers import SignUpSerializer, LoginSerializer, FriendSerializer
from rest_framework.views import APIView
# Create your views here.


class SignUpView(APIView):
    serializer_class = SignUpSerializer

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            # jwt 토큰 접근
            token = TokenObtainPairSerializer.get_token(user)
            refresh_token = str(token)
            access_token = str(token.access_token)
            res = Response(
                {
                    "user": serializer.data,
                    "message": "register successs",
                    "token": {
                        "access": access_token,
                        "refresh": refresh_token,
                    },
                },
                status=status.HTTP_200_OK,
            )

            # jwt 토큰 => 쿠키에 저장
            res.set_cookie("access", access_token, httponly=True)
            res.set_cookie("refresh", refresh_token, httponly=True)

            return res
        return Response({'message': '회원가입 실패', 'data': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    serializer_class = LoginSerializer

    def post(self, request):
        user = authenticate(
            username=request.data.get("username"), password=request.data.get("password")
        )
        # 이미 회원가입 된 유저일 때
        if user is not None:
            serializer = LoginSerializer(user)
            # jwt 토큰 접근
            token = TokenObtainPairSerializer.get_token(user)
            refresh_token = str(token)
            access_token = str(token.access_token)
            res = Response(
                {
                    "user": serializer.data,
                    "message": "login success",
                    "token": {
                        "access": access_token,
                        "refresh": refresh_token,
                    },
                },
                status=status.HTTP_200_OK,
            )
            # jwt 토큰 => 쿠키에 저장
            res.set_cookie("access", access_token, httponly=True)
            res.set_cookie("refresh", refresh_token, httponly=True)
            return res
        else:
            return Response({'message': "존재하지 않는 유저"}, status=status.HTTP_400_BAD_REQUEST)


# class ProfileView(APIView):
#     serializer_class = ProfileSerializer
#
#     def get(self, request):
#         user = request.user
#         data = get_object_or_404(User, pk=user.id)
#
#         serializer = self.serializer_class(data)
#
#         return Response({'message': "프로필 조회 성공", 'data': serializer.validated_data}, status=status.HTTP_200_OK)

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








