# from dataclasses import field
from django.forms import ModelForm,Form
from django.forms import DateTimeField, IntegerField,CharField
from django.forms import ChoiceField
from django.contrib.auth.forms import UserCreationForm,PasswordChangeForm, UserChangeForm
from .models import *

class CreateDriverForm(UserCreationForm):
  class Meta:
    model = CustomUser
    fields = ['username','email','phone_num','license_num','plate_num','max_passenger','vehicle_type','vehicle_brand']
    
class CreatePassengerForm(UserCreationForm):
  class Meta:
    model = CustomUser
    fields = ['username','email','phone_num']
    
class EditPassengerForm(UserChangeForm):
  class Meta:
    model = CustomUser
    fields = ['username','email','phone_num']
    
class EditDriverForm(UserChangeForm):
  class Meta:
    model = CustomUser
    fields = ['username','email','phone_num','license_num','plate_num','max_passenger','vehicle_type','vehicle_brand']
# class PasswordChangeForm(PasswordChangeForm):

class CreatDriverForm_ADD(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ['license_num','plate_num','max_passenger','vehicle_type','vehicle_brand']

class RideRequestForm(ModelForm):
  class Meta:
    model = Ride
    fields = ['start','destination','pick_up_time','arrival_time','shared','vehicle_type','owner_passenger_num','extra_request']