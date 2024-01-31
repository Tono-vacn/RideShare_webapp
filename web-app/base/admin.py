from django.contrib import admin
from .models import CustomUser, Ride, Group, ShareGroupNumberRecord

# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Ride)
admin.site.register(Group)
admin.site.register(ShareGroupNumberRecord)
