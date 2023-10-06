from django import forms

from .models import Teacher
from student.forms import UserInformationForm

class TeacherInformationForm(UserInformationForm):
    teachexp = forms.IntegerField(widget=forms.NumberInput(attrs={'placeholder': 'Enter Your Teaching Experience (In Year)'}), required=False,)
    
    class Meta:
        model = Teacher
        fields = '__all__'
        exclude = ['user']
