from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.contrib import auth
from .models import Profile, Friend

from rest_framework.response import Response
from rest_framework import status
from .serializers import ProfileSerializer
from rest_framework.views import APIView
# Create your views here.


# def signup(request):
#     if request.method == "POST":
#         if request.POST["password1"] == request.POST["password2"]:
#             user = User.objects.create_user(
#                 username=request.POST["username"],
#                 password=request.POST["password1"])
#             nickname = request.POST["nickname"]
#             university = request.POST["university"]
#             enter_year = request.POST["enter_year"]
#             profile = Profile(user=user, nickname=nickname, university=university, enter_year=enter_year)
#             profile.save()
#             auth.login(request,user)
#             return redirect('accounts:home')
#     return render(request, 'accounts/signup.html')
#
#
# def login(request):
#
#     if request.method == "POST":
#         username=request.POST["username"]
#         password=request.POST["password"]
#         user = auth.authenticate(request, username=username, password=password)
#         auth.login(request, user)
#         if user is not None:
#             return redirect('accounts:home')
#         else:
#             return render(request, 'accounts:login', {'error':'not correct'})
#     else:
#         return render(request, 'accounts/login.html')
#
#
# def logout(request):
#     auth.logout(request)
#     return redirect('accounts:home')
#
#
# def home(request):
#     return render(request, 'accounts/home.html')
#
#
# def friend(request):
#     profiles = Profile.objects
#     friends =Friend.objects
#     return render(request, 'accounts/friend.html', {'profiles':profiles, 'friends':friends})
#
# def new_friend(request, profile_id):
#     me = request.user.profile
#     friend = get_object_or_404(Profile, pk=profile_id)
#     new_friend=Friend()
#     new_friend.user=me
#     new_friend.friend=friend
#     if Friend.objects.filter(user=me, friend=friend): # 친구 맺기 해제추가!
#         old_frined=Friend.objects.get(user=me, friend=friend)
#         old_frined.delete()
#     else:
#         new_friend.save()
#     return render(request, 'accounts/home.html')

class ProfileList(APIView):
    def get(self, request, format=None):
        profile=Profile.objects.all()
        serializer=ProfileSerializer(profile, many=True)
        return Response(serializer.data)


