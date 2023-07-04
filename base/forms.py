from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm

from .models import *

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('email','public_visibility','password1','password2','birth_year','address')

class profiledit(ModelForm):
    class Meta:
        model = CustomUser
        fields = ('public_visibility', 'address', 'profilepic')

class newdept(ModelForm):
    class Meta:
        model = Department
        fields = '__all__'

class newdesig(ModelForm):
    class Meta:
        model = Designation
        fields = '__all__'
        exclude = ['department']