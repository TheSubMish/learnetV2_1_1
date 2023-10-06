from django.contrib import admin
from .models import Course,Chapter,Test

# Register your models here.
class CourseAdmin(admin.ModelAdmin):
    list_display = ['courseTitle']
admin.site.register(Course,CourseAdmin)

class ChapterAdmin(admin.ModelAdmin):
    list_display = ['chapterName']
admin.site.register(Chapter,ChapterAdmin)

class TestAdmin(admin.ModelAdmin):
    list_display = ['question']
admin.site.register(Test,TestAdmin)