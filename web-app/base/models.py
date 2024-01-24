# import email
# from email.policy import default
# from pyexpat import model
# from random import choices
# from unittest.util import _MAX_LENGTH
import uuid
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import AbstractUser, AbstractBaseUser, BaseUserManager
from datetime import date
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.

class LoginUserManager(BaseUserManager):
  def create_new_user(self, email_input, psw, first_name = "NULL", last_name = "NULL", phone_num = "+19841234567", user_cata = "PASSENGER", driver_license = "", plate_num = ""):
    if not email_input:
      raise ValueError("invalid email input")
    new_user = self.model(
      first_name = first_name,
      last_name = last_name,
      phone_num = phone_num,
      email = LoginUserManager.normalize_email(email_input),
      psw = psw,
      user_cata = user_cata,
      license_num = driver_license,
      plate_num = plate_num,
    ) 
    new_user.set_password(psw)
    new_user.save(using = self._db)
    return new_user
  
  def create_superuser(self, email, password, first_name = "NULL", last_name = "NULL", phone_num = "+19841234567", user_cata = "PASSENGER", driver_license = "", plate_num = ""):
    sp_user = self.model(
      email = LoginUserManager.normalize_email(email),
      last_name = last_name,
      first_name = first_name,
      user_cata = user_cata,
      phone_num = phone_num,
    )
    
    sp_user.is_admin = True
    sp_user.is_staff = True
    sp_user.is_superuser = True
    sp_user.is_active = True
    sp_user.save(using = self._db)
    return sp_user

class CustomUser(AbstractUser):
  # username = models.CharField(max_length = 64, default = "NULL", help_text = "User Name")
  first_name = models.CharField(max_length = 64, default = "NULL", help_text = "First Name")
  last_name = models.CharField(max_length = 64, default = "NULL", help_text = "Last Name")
  phone_num = PhoneNumberField(default = "+19841234567", primary_key = True)
  email = models.CharField(max_length = 64)
  # user_name = models.CharField(max_length = 20, default = "NULL")
  psw = models.CharField(max_length= 64, default = "NULL")
  USER_CATA = (
    ('Passenger','PASSENGER'),
    ('Driver', 'DRIVER'),
  )
  user_cata = models.CharField(max_length = 10, choices = USER_CATA, default = "Passenger")
  license_num = models.CharField(max_length = 64, null = True, blank = True, help_text = "License Number")
  plate_num = models.CharField(max_length = 20, null = True, blank = True, help_text = "Plate Number")
  max_passenger = models.IntegerField(null = True, blank = True, help_text = "Max Passenger")
  
  VEHICLE_TYPE = (
      ('Economy', '0'),
      ('Comfort', '1'),
      ('Large', '2'),
      ('XL', '3')
  )
  
  vehicle_type = models.CharField(max_length = 20, null=True, blank=True, choices = VEHICLE_TYPE, default = "Economy")
  vehicle_brand = models.CharField(max_length = 20, null=True, blank=True)
  
  objects = LoginUserManager()
  
  USERNAME_FIELD = "phone_num"
  REQUIRED_FIELDS = ["password", "email", "first_name", "last_name", "user_cata"]
  class Meta(AbstractUser.Meta):
    pass
  
class Ride(models.Model):
  id = models.UUIDField(primary_key = True, auto_created = True, default = uuid.uuid4, help_text = "uuid for request")
  start = models.CharField(max_length = 100)
  destination = models.CharField(max_length = 100)
  order_time = models.DateTimeField(auto_now = True)
  pick_up_time = models.DateTimeField(help_text="YYYY-MM-DD HH:MM",null=True, blank = True)
  arrival_time = models.DateTimeField(help_text="YYYY-MM-DD HH:MM",null=True, blank = True)
  # passenger_num = models.IntegerField(null=True)
  owner_passenger_num = models.IntegerField(null=True, blank = True)
  shared = models.BooleanField(default = False)
  driver = models.ForeignKey(CustomUser, on_delete = models.SET_NULL, null = True, blank = True, related_name = 'ride_driver')
  owner = models.ForeignKey(CustomUser, on_delete = models.SET_NULL, null = True, related_name = 'ride_owner')
  extra_request = models.CharField(max_length = 100, null = True, blank = True)  
  
  
  RIDE_STATUS = (('Open','OPEN'),
                 ('Cancelled', 'CANCELLED'),
                 ('Comfirmed','COMFIRMED'),
                 ('In Progress', 'PROGRESS'),
                 ('Completed','COMPLETED'))
  ride_status = models.CharField(max_length = 15, choices = RIDE_STATUS, default = 'open')
  
  def __str__(self):
    return str(self.id)
  
  def get_absolute_url(self):
    return reverse("ride_detail", args = [str(self.id)])
  
class Group(models.Model):
  group_id = models.UUIDField(primary_key=True, auto_created=True, default=uuid.uuid4)
  sharer = models.ForeignKey(CustomUser, on_delete = models.SET_NULL, null = True, related_name = 'group_owner')
  companions = models.ManyToManyField(CustomUser, related_name="participated_group")
  order = models.ForeignKey(CustomUser, on_delete = models.CASCADE, related_name = 'group_order')
  def __str__(self):
    return str(self.group_id)
  def get_absolute_url(self):
      return reverse("order_detail", args = [str(self.group_id)])
  
# class Vehicle(models.Model):