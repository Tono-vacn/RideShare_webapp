# from dataclasses import field
from django.forms import ModelForm,Form
from django.forms import DateTimeField, IntegerField,CharField
from django.forms import ChoiceField
from django.contrib.auth.forms import UserCreationForm,PasswordChangeForm, UserChangeForm
from .models import *

class CreateCustomUserForm(UserCreationForm):
  class Meta:
    model = CustomUser
    fields = ['username','email','phone_num','user_cata','license_num','plate_num']
    
class EditPassengerForm(UserChangeForm):
  class Meta:
    model = CustomUser
    fields = ['username','email','phone_num']
    
class EditDriverForm(UserChangeForm):
  class Meta:
    model = CustomUser
    fields = ['username','email','phone_num','license_num','plate_num','max_passenger','vehicle_type','vehicle_brand']
# class PasswordChangeForm(PasswordChangeForm):

class CreatDriverForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ['license_num','plate_num','max_passenger','vehicle_type','vehicle_brand']

class RideRequestForm(ModelForm):
  pass