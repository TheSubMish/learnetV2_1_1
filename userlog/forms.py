from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate

from .models import CustomUser

class CustomUserForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = ['first_name','last_name','username','email','role']
        labels = {'role': 'Sign-Up as Teacher'}

    first_name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'placeholder': 'First Name'}), required=False,)
    last_name = forms.CharField(max_length=30,widget=forms.TextInput(attrs={'placeholder': 'Last Name'}), required=False)
    username = forms.CharField(max_length=30,widget=forms.TextInput(attrs={'placeholder': 'Username'}), required=False)
    email = forms.EmailField(max_length=30,widget=forms.EmailInput(attrs={'placeholder': 'Enter Your E-Mail'}), required=False)
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}),required=False)
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'}),required=False)
    
class LogInForm(forms.Form):
    username = forms.CharField(max_length=30,widget=forms.TextInput(attrs={'placeholder': 'Username'}),required=False)
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}),required=False)

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')
        if not username:
            raise forms.ValidationError('Username field is required')
        if not password:
            raise forms.ValidationError('Password field is required')
        user = authenticate(username=username, password=password)
        if not user:
            raise forms.ValidationError('Authentication Failed, Incorrect Username or Password')
        return cleaned_data
    
class ContactForm(forms.Form):
    username = forms.CharField(max_length=30,widget=forms.TextInput(attrs={'placeholder':'Username'}),required=False)
    email = forms.EmailField(max_length=30,widget=forms.EmailInput(attrs={'placeholder': 'Enter Your E-Mail'}), required=False)
    message = forms.CharField(widget=forms.Textarea(attrs={'placeholder':'Enter Your Message'}),required=False)

    def clean(self):
        cleaned_data = super().clean()
        
        if not cleaned_data.get('username'):
            raise forms.ValidationError('Username field is required')
        if not cleaned_data.get('email'):
            raise forms.ValidationError('E-mail field is required')
        if not cleaned_data.get('message'):
            raise forms.ValidationError('Message you want to convey?')
        return cleaned_data