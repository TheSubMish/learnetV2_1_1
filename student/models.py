from django.db import models
from userlog.models import CustomUser
from userlog.base import UserBaseClass
from course.models import Course,Test

# Create your models here.
class Student(UserBaseClass):
    user = models.OneToOneField(CustomUser,on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

class UserPreference(models.Model):
    user = models.OneToOneField(Student,on_delete=models.CASCADE)
    html = models.BooleanField(default=False,null=True)
    css = models.BooleanField(default=False,null=True)
    javascript = models.BooleanField(default=False,null=True)
    python = models.BooleanField(default=False,null=True)
    data_analysis = models.BooleanField(default=False,null=True)
    data_structure_and_algorithms = models.BooleanField(default=False,null=True)
    natural_language_processing = models.BooleanField(default=False,null=True)
    machine_learning = models.BooleanField(default=False,null=True)

    def __str__(self):
        return self.user.username
    
class Enroll(models.Model):
    student = models.ForeignKey(Student,on_delete=models.CASCADE)
    course = models.ForeignKey(Course,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.course.courseTitle


class StudentMark(models.Model):
    test = models.ForeignKey(Test,on_delete=models.CASCADE)
    student = models.ForeignKey(Student,on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.test.title