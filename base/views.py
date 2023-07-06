from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm, profiledit, newdept, newdesig
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import get_user_model
from django.contrib import messages
from .models import Department, Designation, CustomUser
from django.core import serializers

User = get_user_model()

# Create your views here.

def home(request):
    return render(request, 'base/home.html')

def registeruser(request):      #used to register new users
    form = CustomUserCreationForm()     #using a custom creation form

    if request.method == 'POST':        #if the form was submitted with the post method
        form = CustomUserCreationForm(request.POST)     #we input the data submitted in the form and input it in the backend form
        if form.is_valid():     #if all the data entered was valid then proceed
            user = form.save()      #we save the form and login the user
            login(request,user)
            return redirect('home')     #if registration was successful then goto home
        else:
            messages.error(request, 'error occured')    #if not then raise error

    context = {'form':form}     #we send the custom form to the frontend
    return render(request, 'base/register.html', context)

def loginuser(request):     #used to login an existing user

    page = 'login'      #this is used to satisfy a condition in the navbar

    if request.user.is_authenticated:       #if the user is already authenticated the goto home 
        return redirect('home')

    if request.method == 'POST':        #if the login form was submitted
        email = request.POST.get('email')       #get the required information 
        password = request.POST.get('password')     

        try:        #here we check if the email provided is registed with the database
            email = User.objects.get(email=email)
        except:
            messages.error(request, 'No matching email')
        
        user = authenticate(request, email=email, password=password)    #if all goes well then authenticate the user 

        if user is not None:    #if the user exists then log them in and goto home page
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
        form = profiledit(request.POST, request.FILES, instance=user)   #request.FILES is used to get the image that was uploaded
        if form.is_valid():
            form.save()
        dept = request.POST.get('dept')
        desig = request.POST.get('desig')
        manager = request.POST.get('manager')
        if dept != 'null':
            user.department = Department.objects.get(name=dept)     #we set the department of the user(id) to the department id of the selected field in the html repsonse
        else:
            user.department = None
        
        if desig != None:
            user.designation = Designation.objects.get(pk=desig)        #we set the department of the user(id) to the department id of the selected field in the html repsonse
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

def createdepartment(request):      #this view is used to create a new department in the database
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

def createdesignation(request):         #this view is used to create a new designation for a department int the database
    user = request.user
    desigs = Designation.objects.all()
    depts = Department.objects.all()

    formdesig = newdesig()


    if request.method == 'POST':
        dept = request.POST.get('dept')
        if dept != 'null':
            department = Department.objects.get(name=dept)      #getting the department which the user submitted 
            Designation.objects.create(
            department = department,
            Title = request.POST.get('Title')
            )
        return redirect('profile', pk=user.id)

    context = {'formdesig':formdesig, 'desigs':desigs, 'depts':depts}
    return render(request, 'base/designation_form.html', context)

def get_designations(request):      #this is the api called by the AJAX request which provides dynamic designations to the user base on their role and the selected department
    user = request.user     
    allusers = CustomUser.objects.all()
    departments = request.GET.get('department')     #we get the selected department from the request sent by AJAX
    designations = Designation.objects.filter(department__name = departments)       #we get the designation which are related to the selected department
    options = ''

    for designation in designations:    #looping through all the available desingations
        manager_exists = False      #initially setting to false
        if designation.Title == 'Manager':      #if loop comes across the Manager title
            for users in allusers:      #we search for all users
                if users.department != None and users.department.name == departments and users.designation.Title == 'Manager':      #if the user is a manager of the selected department then
                    if (user.department == None) or (user.department.name != departments or (user.department.name == departments and user.designation.Title != 'Manager')):     #if logged in user does not belong to a department or the user belongs to a different department or the logged in user belongs to the same department and is not the manager of the department
                        manager_exists = True   #then we want to exlude the manager from the list
        
        if manager_exists == False:
            if user.designation != None:    #then we just concatenate the values to the object string to be sent as the options for the selection in the html form
                options += f'<option value="{designation.pk}" {"selected" if designation.Title == user.designation.Title else ""}>{designation.Title}</option>'
            else:
                options += f'<option value="{designation.pk}">{designation.Title}</option>'

    return HttpResponse(options)    #TODO:Change the HTTPResponse to JSONResponse

def get_managers(request):
    users = CustomUser.objects.all()
    departments = request.GET.get('department')
    options = ''

    for user in users:
        if user.designation != None:
            if user.designation.Title == 'Manager' and user.department.name == departments and user != request.user:        #if the user is manager of a department and is not logged in then add the user as an option of manager
                options += f'<option value="{user.first_name}" {"selected" if user.first_name == request.user.manager else ""}>{user.first_name}</option>'


    return HttpResponse(options)

def get_users(request):
    users = CustomUser.objects.all()    
    data = serializers.serialize("json", users)     #used to convert a queryset or list of objects into JSON serialized data
    return JsonResponse(data, safe=False)