from django.db import models

from userlog.models import CustomUser
from userlog.base import UserBaseClass
# Create your models here.

class Teacher(UserBaseClass):
    user = models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    teachexp = models.IntegerField(null=True)

    def __str__(self):
        return self.user.username