from django import forms
from .models import Student,UserPreference
from django.core.validators import RegexValidator

class UserInformationForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30,widget=forms.TextInput(attrs={'placeholder': 'First Name'}),required=False,)
    last_name = forms.CharField(max_length=30,widget=forms.TextInput(attrs={'placeholder': 'Last Name'}),required=False)

    class Meta:
        model = Student
        fields = '__all__'
        exclude = ['user']

    phone = forms.CharField(
        widget=forms.TextInput(attrs={
            'placeholder': 'Phone Number'
        }),
        required=False,
        validators=[
            RegexValidator(
                '(\+977)?[9][6-9]\d{8}',
                message='Phone Number should be in "+977-9800000000"'
            )]
        )
    city = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'placeholder': 'Enter Your City Name'}), required=False,)
    district = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'placeholder': 'Enter Your District Name'}), required=False,)
    state = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'placeholder': 'Enter Your State Name'}), required=False,)

    def clean(self):
        cleaned_data = super().clean()
        first_name = cleaned_data.get('first_name')
        last_name = cleaned_data.get('last_name')

        if not first_name:
            raise forms.ValidationError('First Name field is required')
        if not last_name:
            raise forms.ValidationError('Last Name field is required')
        
        return cleaned_data
            

class UserPreferenceForm(forms.ModelForm):
    
    class Meta:
        model = UserPreference
        fields = '__all__'
        exclude = ['user']

    html = forms.BooleanField(required=False,label='html',widget=forms.CheckboxInput())
    css = forms.BooleanField(required=False,label='css',widget=forms.CheckboxInput())
    javascript = forms.BooleanField(required=False,label='javascript',widget=forms.CheckboxInput())
    python = forms.BooleanField(required=False, label='python',widget=forms.CheckboxInput())
    data_analysis = forms.BooleanField(required=False, label='data analysis',widget=forms.CheckboxInput())
    data_structure_and_algorithms = forms.BooleanField(required=False, label='data structure and algorithms',widget=forms.CheckboxInput())
    natural_language_processing = forms.BooleanField(required=False, label='natural language processing',widget=forms.CheckboxInput())
    machine_learning = forms.BooleanField(required=False,label='machine learning',widget=forms.CheckboxInput())