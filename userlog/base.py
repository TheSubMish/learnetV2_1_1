from django.db import models

def image_validation(instance,filename):
    # image
    picName = instance.profilepic
    ext = picName.name.split('.')[-1]
    # person
    name = instance.user
    filename = f"{name}.{ext}"

    return filename if ext in ["png", "jpg", "jpeg"] else "error"

# choices for educational background
eduback_choices = (
    ("1","Higher Secondary"),
    ("2","Diploma or Certificate Programs"),
    ("3","Bachelor's Degree"),
    ("4","Master's Degree"),
    ("5","Doctoral Degree (Ph.D.)")
)

class UserBaseClass(models.Model):
    profilepic = models.ImageField(default='profilepic\profile.jpg',upload_to='profilepic/')
    phone = models.CharField(blank=True, null=True,max_length=15)
    city = models.CharField(max_length=30,null=True)
    district = models.CharField(max_length=30,null=True)
    state = models.CharField(max_length=30,null=True)
    edubackground = models.CharField(max_length=30,choices=eduback_choices,default='1',null=True)

    class Meta:
        abstract = True