from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth
from .models import Profile
# Create your views here.


def signup(request):
    if request.method == "POST":
        if request.POST["password1"] == request.POST["password2"]:
            user = User.objects.create_user(
                username=request.POST["username"],
                password=request.POST["password1"])
            nickname = request.POST["nickname"]
            university = request.POST["university"]
            enter_year = request.POST["enter_year"]
            profile = Profile(user=user, nickname=nickname, university=university, enter_year=enter_year)
            profile.save()
            auth.login(request,user)
            return redirect('accounts:home')
    return render(request, 'accounts/signup.html')


def login(request):

    if request.method == "POST":
        username=request.POST["username"]
        password=request.POST["password"]
        user = auth.authenticate(request, username=username, password=password)
        auth.login(request, user)
        if user is not None:
            return redirect('accounts:home')
        else:
            return render(request, 'accounts:login', {'error':'not correct'})
    else:
        return render(request, 'accounts/login.html')


def logout(request):
    auth.logout(request)
    return redirect('accounts:home')


def home(request):
    return render(request, 'accounts/home.html')
