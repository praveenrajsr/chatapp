from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from customuser.models import CustomUser

def dashboard(request):
    return HttpResponse("Working")

def chat_box(request):
    return render(request, "chatapp/chatbox.html")

def login(request):
    if request.user.is_authenticated:
        return redirect(chat_box)
    else:
        return render(request, 'auth/login.html')

def dashboard(request):
    users = CustomUser.objects.all()
    return render(request, "chatapp/dashboard.html ", {"users": users})