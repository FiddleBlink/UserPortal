from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm, ModelChoiceField, Form
from .models import *

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('first_name', 'email', 'birth_year','password1','password2')

class profiledit(ModelForm):
    class Meta:
        model = CustomUser
        fields = ('first_name', 'profilepic', 'public_visibility', 'address')

class newdept(ModelForm):
    class Meta:
        model = Department
        fields = '__all__'

class newdesig(ModelForm):
    class Meta:
        model = Designation
        fields = '__all__'
        exclude = ['department']
