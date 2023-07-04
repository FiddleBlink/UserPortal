from django.db import models
from django.contrib.auth.models import AbstractUser
from .manager import *

# Create your models here.

class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    public_visibility = models.BooleanField(default=False)
    birth_year = models.CharField(max_length=4)
    address = models.TextField(null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

