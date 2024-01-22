import email
from email.policy import default
from random import choices
from unittest.util import _MAX_LENGTH
from django.db import models
from django.contrib.auth.models import AbstractUser, AbstractBaseUser, BaseUserManager
from datetime import date
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.

class LoginUserManager(BaseUserManager):
  def create_new_user(self, email_input, psw, first_name = "NULL", last_name = "NULL", phone_num = "+19841234567", user_group = "PASSENGER", driver_license = "", plate_num = ""):
    if not email_input:
      raise ValueError("invalid email input")
    new_user = self.model(
      first_name = first_name,
      last_name = last_name,
      phone_num = phone_num,
      email = LoginUserManager.normalize_email(email_input),
      psw = psw,
      user_group = user_group,
      license_num = driver_license,
      plate_num = plate_num,
    ) 
    new_user.set_password(psw)
    new_user.save(using = self._db)
    return new_user
  
  def create_super_user(self, email_input, psw, first_name = "NULL", last_name = "NULL", phone_num = "+19841234567", user_group = "PASSENGER", driver_license = "", plate_num = ""):
    sp_user = self.model(
      email = LoginUserManager.normalize_email(email_input),
      last_name = last_name,
      first_name = first_name,
      user_group = user_group,
      phone_num = phone_num,
    )
    
    sp_user.is_admin = True
    sp_user.is_staff = True
    sp_user.is_superuser = True
    sp_user.is_active = True
    sp_user.save(using = self._db)
    return sp_user

class User(AbstractUser):
  first_name = models.CharField(max_length = 64, default = "NULL", help_text = "First Name")
  last_name = models.CharField(max_length = 64, default = "NULL", help_text = "Last Name")
  phone_num = PhoneNumberField(default = "+19841234567", primary_key = True)
  email = models.CharField(max_length = 64)
  # user_name = models.CharField(max_length = 20, default = "NULL")
  psw = models.CharField(max_length= 64, default = "NULL")
  USER_GROUP = (
    ('Passenger','PASSENGER'),
    ('Driver', 'DRIVER'),
  )
  user_group = models.CharField(max_length = 10, choices = USER_GROUP, default = "Passenger")
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
  REQUIRED_FIELDS = ["password", "email", "first_name", "last_name", "user_group"]
  class Meta(AbstractUser.Meta):
    pass
  
# class Vehicle(models.Model):