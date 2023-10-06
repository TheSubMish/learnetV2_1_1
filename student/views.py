from django.shortcuts import render,redirect
from django.views.generic import CreateView,ListView,FormView
from django.views.generic.detail import DetailView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Max
import json
from django.core.mail import send_mail

from .forms import UserInformationForm,UserPreferenceForm
from .models import Student,UserPreference,Enroll,StudentMark
from userlog.models import CustomUser
from userlog.forms import ContactForm
from course.models import Course,Chapter,Test
from .get_or_create import get_user_information,get_user_preferences,save_user_name,update_user_information,create_pref,update_pref

# Create your views here.
class StudentDashboard(LoginRequiredMixin,CreateView):
    login_url = '/login/'
    template_name = 'studash.html'
    success_url = reverse_lazy('student_dashboard')
    userform = UserInformationForm
    prefForm = UserPreferenceForm

    def get(self,request,error=None):
        username = request.user.username
        try:
            currentuser = CustomUser.objects.get(username=username)
            currentuserinfo = Student.objects.get(user=currentuser)
        except Student.DoesNotExist:
            return redirect(self.login_url)

        # get current user informations from database main code is in get_or_create.py    
        self.userform = get_user_information(currentuser,currentuserinfo)
        # get current user preferences from database main code is in get_or_create.py
        userPref = get_user_preferences(request)
        if userPref is None:
            return render(request,self.template_name,{'userform':self.userform,'prefform': self.prefForm,'pic':currentuserinfo,'error':error})
        else:
            self.prefForm = userPref
            return render(request,self.template_name,{'userform':self.userform,'prefform': self.prefForm,'pic':currentuserinfo,'error':error})
        
    def post(self,request,error=None):
        user_info_form_data = self.userform(request.POST,request.FILES)
        if user_info_form_data.is_valid():
            save_user_name(user_info_form_data.cleaned_data,request.user.username)
            if user:=Student.objects.get(user=request.user):
                update_user_information(user_info_form_data.cleaned_data,user)
            else:
                user_info_form_data.save()
        else:
            error_msg_dict = json.loads(user_info_form_data.errors.as_json())
            if error_msg_dict['phone']:
                error_msg = error_msg_dict['phone'][0]['message']
            else:
                error_msg = error_msg_dict['__all__'][0]['message']
            return redirect('student_dashboard_error',error_msg)
        
        user_preferences_data = self.prefForm(request.POST)
        if user_preferences_data.is_valid():
            user = Student.objects.get(user=request.user)
            try:
                prefUser=UserPreference.objects.get(user=user)
                update_pref(user_preferences_data.cleaned_data,prefUser)
            except UserPreference.DoesNotExist:
                create_pref(user_preferences_data.cleaned_data,user)
            return redirect(self.success_url)
        

class AllCourses(ListView):
    template_name = 'manycourse.html'
    model = Course
    context_object_name = 'courses'
    
class SingleCourse(DetailView):
    template_name = 'singleCourse.html'
    model = Course
    context_object_name = 'course'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course = Course.objects.get(slug=self.kwargs['slug'])
        context['course'] = course
        context['chapter'] = Chapter.objects.filter(course=course).first()
        return context

class ReadCourse(LoginRequiredMixin,DetailView):
    login_url = '/login/'
    template_name = 'course.html'
    model = Chapter
    context_object_name = 'chapter'

    def dispatch(self, request, *args, **kwargs):
        try:
            student = Student.objects.get(user=request.user)
        except:
            return redirect(self.login_url)
        course = Course.objects.get(slug=self.kwargs['slug'])
        # Create or get the enrollment
        enrollment, enrollment_created = Enroll.objects.get_or_create(student=student, course=course)
        return super().dispatch(request, *args, **kwargs)
    

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        course = Course.objects.get(slug=self.kwargs['slug'])
        context['chapters'] = Chapter.objects.filter(course=course)
        context['tests'] = Test.objects.filter(course=course).order_by('title').values('title').annotate(max_id=Max('id'))
        context['course'] = course
        return context
    
class GiveTest(LoginRequiredMixin,DetailView):
    login_url = '/login/'
    template_name = 'test.html'
    model = Test

    def dispatch(self, request, *args, **kwargs):
        try:
            Student.objects.get(user=request.user)
        except:
            return redirect(self.login_url)
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        course = Course.objects.get(slug=self.kwargs['slug'])
        context['course'] = course
        context['chapters'] = Chapter.objects.filter(course=course)
        context['tests'] = Test.objects.filter(course=course).order_by('title').values('title').annotate(max_id=Max('id'))
        context['current_test'] = Test.objects.filter(title=self.kwargs['title'])
        student = Student.objects.get(user=self.request.user)
        try:
            score = StudentMark.objects.get(test=context['current_test'][:1].get(),student=student).score
        except StudentMark.DoesNotExist:
            score = 0
        context['score'] = score
        return context
    
    def post(self,request,slug=None,pk=None,title=None):
        field_values,score = [],0
        total_questions = Test.objects.filter(title = title).values('question').distinct().count()
        for i in range(1, total_questions + 1):
            field_name = f'option{i}'
            field_value = request.POST.getlist(field_name)
            field_values.extend(field_value)
        corAns = Test.objects.filter(title = title).values_list('corAns', flat=True).order_by('-id')
        for i,item in enumerate(field_values):
            if item == corAns[i]:
                score = score + 1
        test = Test.objects.get(pk=pk)
        student = Student.objects.get(user=request.user)
        try:
            score_update = StudentMark.objects.get(test=test,student=student)
            score_update.score = score
            score_update.save()
        except StudentMark.DoesNotExist:
            StudentMark.objects.create(test=test,student=student,score=score)
        url = reverse_lazy('give_test', kwargs={'slug':slug,'pk':pk,'title':title})
        return redirect(url)
    
class StudentContact(FormView):
    template_name = 'contact.html'
    form_class = ContactForm

    def form_invalid(self, form):
        error = {'username':'','email':'','message':''}
        error_msg_dict = json.loads(form.errors.as_json())
        error_msg = error_msg_dict['__all__'][0]['message']
        if 'Username' in error_msg:
            error['username'] = error_msg
        if 'E-mail' in error_msg:
            error['email'] = error_msg
        if 'Message' in error_msg:
            error['message'] = error_msg
        return render(self.request,self.template_name,{'form':form,'error':error})
    
    def form_valid(self,form):
        from_email = self.request.POST['email']
        subject = "Message from " + from_email
        message = self.request.POST['message']
        recipient_email = 'sumi_csit2077@lict.edu.np'
        send_mail(subject,message,from_email,[recipient_email])
        return redirect('student_contact')