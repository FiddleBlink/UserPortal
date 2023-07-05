from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm, profiledit, newdept, newdesig
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from django.contrib import messages
from .models import Department, Designation, CustomUser

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
    return redirect('login')

def userprofile(request, pk):
    user = request.user
    depts = Department.objects.all()
    desigs = Designation.objects.all()
    users = CustomUser.objects.all()

    form = profiledit(instance=user)    

    if request.method == 'POST':
        form = profiledit(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
        dept = request.POST.get('dept')
        desig = request.POST.get('desig')
        manager = request.POST.get('manager')
        if dept != 'null':
            user.department = Department.objects.get(name=dept)
        else:
            user.department = None
        
        if desig != None:
            user.designation = Designation.objects.get(pk=desig)
        else:
            user.designation = None

        if manager != None:
            user.manager = manager
        else:
            user.manager = None

        user.save()

        return redirect('home')

    context = {'form':form, 'depts':depts, 'desigs':desigs, 'users':users}
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
    depts = Department.objects.all()

    formdesig = newdesig()


    if request.method == 'POST':
        dept = request.POST.get('dept')
        if dept != 'null':
            department = Department.objects.get(name=dept)
            Designation.objects.create(
            department = department,
            Title = request.POST.get('Title')
            )
        return redirect('profile', pk=user.id)

    context = {'formdesig':formdesig, 'desigs':desigs, 'depts':depts}
    return render(request, 'base/designation_form.html', context)

def get_designations(request):
    user = request.user
    allusers = CustomUser.objects.all()
    departments = request.GET.get('department')
    designations = Designation.objects.filter(department__name = departments)
    options = ''

    for designation in designations:
        is_manager = False
        if designation.Title == 'Manager':
            for users in allusers:
                if users.department != None:
                    if users.designation.Title == 'Manager' and users.department.name == departments:
                        if user.designation == None or user.designation.Title != 'Manager':
                                is_manager = True
        
        if is_manager == False:
            if user.designation != None:
                options += f'<option value="{designation.pk}" {"selected" if designation.Title == user.designation.Title else ""}>{designation.Title}</option>'
            else:
                options += f'<option value="{designation.pk}">{designation.Title}</option>'


    return HttpResponse(options)

def get_managers(request):
    users = CustomUser.objects.all()
    departments = request.GET.get('department')
    options = ''

    for user in users:
        if user.designation != None:
            if user.designation.Title == 'Manager' and user.department.name == departments and user != request.user:
                options += f'<option value="{user.first_name}" {"selected" if user.first_name == request.user.manager else ""}>{user.first_name}</option>'


    return HttpResponse(options)