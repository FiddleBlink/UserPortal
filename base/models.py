from django.db import models
from django.contrib.auth.models import AbstractUser
from .manager import *

# Create your models here.

class Department(models.Model):
    name = models.CharField(max_length=100)

class Designation(models.Model):
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)
    Title = models.CharField(max_length=100)

class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    public_visibility = models.BooleanField(default=False)
    birth_year = models.CharField(max_length=4)
    address = models.TextField(null=True, blank= True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True, blank=True)
    designation = models.ForeignKey(Designation, on_delete=models.CASCADE, null=True, blank=True)
    manager = models.CharField(max_length=100, null=True, blank=True)
    profilepic = models.ImageField(upload_to='uploads/')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()