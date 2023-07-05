from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    path('login/', views.loginuser, name='login'),
    path('register/', views.registeruser, name='register'),
    path('logout/', views.logoutuser, name='logout'),

    path('profile/<str:pk>/' , views.userprofile, name='profile'),

    path('designation/', views.createdepartment, name='department'),
    path('department/', views.createdesignation, name='designation'),

    path('getdesig/', views.get_designations, name="getdesigs"),
    path('getmanager/', views.get_managers, name="getmanager")
]
