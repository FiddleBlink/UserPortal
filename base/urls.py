from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    path('login/', views.loginuser, name='login'),
    path('register/', views.registeruser, name='register'),
    path('logout/', views.logoutuser, name='logout')
]
