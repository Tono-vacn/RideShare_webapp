# from dataclasses import field
from django.forms import ModelForm,Form
from django.forms import DateTimeField, IntegerField,CharField
from django.forms import ChoiceField
from django.contrib.auth.forms import UserCreationForm,PasswordChangeForm
from .models import *

class CreateCustomUserForm(UserCreationForm):
  class Meta:
    model = CustomUser
    fields = ['username','email','phone_num','user_cata','license_num','plate_num']
    
class EditCustomUserForm(UserCreationForm):
  class Meta:
    model = CustomUser
    fields = ['username','email','phone_num','user_cata','license_num','plate_num']
    
class RideRequestForm(ModelForm):
  pass