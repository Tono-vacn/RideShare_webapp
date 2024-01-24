from django.contrib import admin
from .models import CustomUser, Ride, RideGroup

# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Ride)
admin.site.register(RideGroup)
