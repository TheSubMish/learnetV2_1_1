from django.contrib import admin
from .models import CustomUser

# Register your models here.
class CustomUserModel(admin.ModelAdmin):
    list_display = ['username','first_name','last_name','email','is_staff']
admin.site.register(CustomUser,CustomUserModel)
