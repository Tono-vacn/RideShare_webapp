import uuid
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import AbstractUser, AbstractBaseUser, BaseUserManager
from datetime import date
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.

class LoginUserManager(BaseUserManager):
  def create_new_user(self, email_input, psw, username = "NULL", phone_num = "+19841234567", user_cata = "PASSENGER", driver_license = "", plate_num = "", max_passenger = 0, vehicle_type = "Economy", vehicle_brand = "NULL"):
    if not email_input:
      raise ValueError("invalid email input")
    new_user = self.model(
      username = username,
      phone_num = phone_num,
      email = LoginUserManager.normalize_email(email_input),
      psw = psw,
      user_cata = user_cata,
      license_num = driver_license,
      plate_num = plate_num,
      max_passenger = max_passenger,
      vehicle_type = vehicle_type,
      vehicle_brand = vehicle_brand,
    ) 
    new_user.set_password(psw)
    new_user.save(using = self._db)
    return new_user
  

class CustomUser(AbstractUser):
  username = models.CharField(max_length = 64, default = "NULL", help_text = "User Name", unique=True)
  phone_num = PhoneNumberField(default = "+19841234567")
  email = models.CharField(max_length = 64)
  USER_CATA = (
    ('Passenger','Passenger'),
    ('Driver', 'Driver'),
  )
  user_cata = models.CharField(max_length = 10, choices = USER_CATA, default = "Passenger")
  license_num = models.CharField(max_length = 64, null = True, blank = True, help_text = "License Number")
  plate_num = models.CharField(max_length = 20, null = True, blank = True, help_text = "Plate Number")
  max_passenger = models.IntegerField(null = True, blank = True, help_text = "Max Passenger")
  
  VEHICLE_TYPE = (
      ('Economy', 'Economy'),
      ('Comfort', 'Comfort'),
      ('Large', 'Large'),
      ('XL', 'XL')
  )
  
  vehicle_type = models.CharField(max_length = 20, null=True, blank=True, choices = VEHICLE_TYPE, default = "Economy")
  vehicle_brand = models.CharField(max_length = 20, null=True, blank=True)
  
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
  # number of owner group
  owner_passenger_num = models.IntegerField(null=True, blank = True)
  shared = models.BooleanField(default = False)
  driver = models.ForeignKey(CustomUser, on_delete = models.SET_NULL, null = True, blank = True, related_name = 'ride_driver')
  owner = models.ForeignKey(CustomUser, on_delete = models.SET_NULL, null = True, related_name = 'ride_owner')
  extra_request = models.CharField(max_length = 100, null = True, blank = True)  
  ride_group = models.ForeignKey('Group', on_delete = models.SET_NULL, null = True, blank = True, related_name = 'ride_group')
  
  RIDE_STATUS = (('OPEN','OPEN'),
                 ('CANCELLED', 'CANCELLED'),
                 ('CONFIRMED','CONFIRMED'),
                 ('PROGRESS', 'PROGRESS'),
                 ('COMPLETED','COMPLETED'))
  ride_status = models.CharField(max_length = 15, choices = RIDE_STATUS, default = 'OPEN')
  
  VEHICLE_TYPE = (
      ('Economy', 'Economy'),
      ('Comfort', 'Comfort'),
      ('Large', 'Large'),
      ('XL', 'XL')
  )
  
  vehicle_type = models.CharField(max_length = 20, null=True, blank=True, choices = VEHICLE_TYPE, default = "Economy")
  
  def __str__(self):
    return str(self.id)
  
  def get_absolute_url(self):
    return reverse("ride_detail", args = [str(self.id)])
  
class Group(models.Model):
  group_id = models.UUIDField(primary_key=True, auto_created=True, default=uuid.uuid4)
  sharer = models.ForeignKey(CustomUser, on_delete = models.SET_NULL, null = True, related_name = 'group_owner')
  companions = models.ManyToManyField(CustomUser, related_name="participated_group", blank = True, null=True)
  order = models.ForeignKey(Ride, on_delete = models.CASCADE, related_name = 'group_order',blank = True, null=True)
  total_group_num = models.IntegerField(null = True, blank = True)
  def __str__(self):
    return str(self.group_id)
  def get_absolute_url(self):
      return reverse("order_detail", args = [str(self.group_id)])
    
class ShareGroupNumberRecord(models.Model):
  group = models.ForeignKey(Group, on_delete = models.CASCADE,null = True, blank = True)
  order = models.ForeignKey(Ride, on_delete = models.CASCADE,null = True, blank = True)
  sharer = models.ForeignKey(CustomUser, on_delete = models.CASCADE,null = True, blank = True)
  share_num = models.IntegerField(null = True, blank = True)
  
