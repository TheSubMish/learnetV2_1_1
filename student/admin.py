from django.contrib import admin
from .models import Student,UserPreference,Enroll,StudentMark
# Register your models here.
class StudentAdmin(admin.ModelAdmin):
    list_display = ['user']
admin.site.register(Student,StudentAdmin)

class UserPreferenceAdmin(admin.ModelAdmin):
    list_display = ['user']
admin.site.register(UserPreference,UserPreferenceAdmin)

class EnrollAdmin(admin.ModelAdmin):
    list_display=['student','course']
admin.site.register(Enroll,EnrollAdmin)

class StudentMarkAdmin(admin.ModelAdmin):
    list_display=['student','test']
admin.site.register(StudentMark,StudentMarkAdmin)