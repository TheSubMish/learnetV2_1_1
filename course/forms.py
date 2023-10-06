from django import forms

from .models import Course,cousreCategory,Chapter,Test

class CourseForm(forms.ModelForm):

    class Meta:
        model = Course
        fields = '__all__'
        exclude = ['teacher','slug']

    courseTitle = forms.CharField(max_length=100,widget=forms.TextInput(attrs={'placeholder':'Enter Your Course Name'}),required=False)
    courseDescrip = forms.CharField(widget=forms.Textarea(attrs={'placeholder':'Enter Your Course Description'}),required=False)
    category = forms.ChoiceField(required=False,choices=cousreCategory,label='Select Category Of Cousre')
    courseImage = forms.ImageField(required=False,label='Course Image')

    def clean(self):
        cleaned_data = super().clean()
        if not cleaned_data.get('courseTitle'):
            raise forms.ValidationError('Course Name Cannot Be Empty')
        if not cleaned_data.get('courseDescrip'):
            raise forms.ValidationError('Course Description Cannot Be Empty')
        if not cleaned_data.get('courseImage'):
            raise forms.ValidationError('Image Field Cannot Be Empty')
        return cleaned_data

class ChapterForm(forms.ModelForm):

    class Meta:
        model = Chapter
        fields = '__all__'
        
    chapterName = forms.CharField(max_length=100,required=False,widget=forms.TextInput(attrs={'placeholder':'Enter Chapter Name'}))
    chapterBody = forms.CharField(required=False,widget=forms.Textarea(attrs={'placeholder':'Enter Chapter Content'}))
    add_more = forms.BooleanField(required=False, widget=forms.HiddenInput(), initial=False)
    next = forms.BooleanField(required=False, widget=forms.HiddenInput(), initial=False)

    def clean(self):
        cleaned_data = super().clean()
        if not cleaned_data.get('course'):
            raise forms.ValidationError('Course Name Cannot Be Empty')
        if not cleaned_data.get('chapterName'):
            raise forms.ValidationError('Chapter Name Cannot Be Empty')
        if not cleaned_data.get('chapterBody'):
            raise forms.ValidationError('Chapter Content Cannot Be Empty')
        return cleaned_data
    
    def __init__(self, *args, **kwargs):
        teacher_courses = kwargs.pop('teacher_courses', None)
        super().__init__(*args, **kwargs)

        if teacher_courses:
            self.fields['course'].queryset = teacher_courses
    

class TestForm(forms.ModelForm):

    class Meta:
        model = Test
        fields = '__all__'

    title = forms.CharField(max_length=100,required=False,widget=forms.TextInput(attrs={'placeholder':'Enter Test Title'}))
    question = forms.CharField(max_length=200,required=False,widget=forms.TextInput(attrs={'placeholder':'Test Question'}))
    option1 = forms.CharField(max_length=100,required=False,widget=forms.TextInput(attrs={'placeholder':'Enter Option One'}))
    option2 = forms.CharField(max_length=100,required=False,widget=forms.TextInput(attrs={'placeholder':'Enter Option Two'}))
    option3 = forms.CharField(max_length=100,required=False,widget=forms.TextInput(attrs={'placeholder':'Enter Option Three'}))
    option4 = forms.CharField(max_length=100,required=False,widget=forms.TextInput(attrs={'placeholder':'Enter Option Four'}))
    corAns = forms.CharField(max_length=100,required=False,widget=forms.TextInput(attrs={'placeholder':'Enter Correct Answer'}))
    add_more = forms.BooleanField(required=False, widget=forms.HiddenInput(), initial=False)
    publish = forms.BooleanField(required=False, widget=forms.HiddenInput(), initial=False)

    def clean(self):
        cleaned_data = super().clean()
        if not cleaned_data.get('course'):
            raise forms.ValidationError('Course Name Cannot Be Empty')
        if not cleaned_data.get('title'):
            raise forms.ValidationError('Test Title Field Cannot Be Empty')
        if not cleaned_data.get('question'):
            raise forms.ValidationError('Question Field Cannot Be Empty')
        if not cleaned_data.get('option1'):
            raise forms.ValidationError('Option One Field Cannot Be Empty')
        if not cleaned_data.get('option2'):
            raise forms.ValidationError('Option Two Field Cannot Be Empty')
        if not cleaned_data.get('option3'):
            raise forms.ValidationError('Option Three Field Cannot Be Empty')
        if not cleaned_data.get('option4'):
            raise forms.ValidationError('Option Four Field Cannot Be Empty')
        if not cleaned_data.get('corAns'):
            raise forms.ValidationError('Correct Answer Field Cannot Be Empty')
        return cleaned_data
    
    def __init__(self, *args, **kwargs):
        teacher_courses = kwargs.pop('teacher_courses', None)
        super().__init__(*args, **kwargs)

        if teacher_courses:
            self.fields['course'].queryset = teacher_courses