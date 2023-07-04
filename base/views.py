from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm, profiledit, newdept, newdesig
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from django.contrib import messages
from .models import Department, Designation

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

def userprofile(request, pk):
    user = request.user

    form = profiledit(instance=user)    

    if request.method == 'POST':
        form = profiledit(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('home')

        return redirect('profile', pk=user.id)

    context = {'form':form}
    return render(request, 'base/profile.html', context)

def createdepartment(request):
    user = request.user
    depts = Department.objects.all()

    formdept = newdept()
    
    if request.method == 'POST':
        Department.objects.create(
            name = request.POST.get('name')
        )
        return redirect('profile', pk=user.id)

    context = {'formdept':formdept, 'depts':depts}
    return render(request, 'base/department_form.html', context)

def createdesignation(request):
    user = request.user
    desigs = Designation.objects.all()

    formdesig = newdesig()


    if request.method == 'POST':
        dept = request.POST.get('dept')
        try:
            department = Department.objects.get(name=dept)
            Designation.objects.create(
            department = department,
            Title = request.POST.get('Title')
        )
        except:
            messages.error(request, 'error creating designation')
        return redirect('profile', pk=user.id)

    context = {'formdesig':formdesig, 'desigs':desigs}
    return render(request, 'base/designation_form.html', context)