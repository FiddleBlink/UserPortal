from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from django.contrib import messages

User = get_user_model()

# Create your views here.

def home(request):
    return render(request, 'base/home.html')

def registeruser(request):
    form = CustomUserCreationForm()

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request,user)
            return redirect('home')
        else:
            messages.error(request, 'error occured')

    context = {'form':form}
    return render(request, 'base/register.html', context)

def loginuser(request):

    page = 'login'

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            email = User.objects.get(email=email)
        except:
            messages.error(request, 'No matching email')
        
        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password')

    context={'page':page}
    return render(request, 'base/login.html', context)

def logoutuser(request):
    logout(request)
    return redirect('home')