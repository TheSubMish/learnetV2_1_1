from django.shortcuts import render,redirect
from django.views.generic import FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
import json
from django.core.mail import send_mail

from .models import Teacher
from .forms import TeacherInformationForm
from student.get_or_create import get_user_information,save_user_name,update_user_information
from course.models import Course
from student.views import StudentContact
from userlog.forms import ContactForm
# Create your views here.

class TeacherDashboard(LoginRequiredMixin,FormView):
    login_url = '/login/'
    template_name = 'teachdash.html'
    form_class = TeacherInformationForm
    model = Teacher
    success_url = reverse_lazy('teacher_dashboard')
    def get(self,request,error=None):
        # get current user informations from database main code is in get_or_create.py
        try:
            currentuserinfo = Teacher.objects.get(user=request.user)
        except Teacher.DoesNotExist:
            return redirect(self.login_url)
        
        courses = Course.objects.filter(teacher=currentuserinfo).order_by('-id')[:4]
        
        self.form_class = get_user_information(request.user,currentuserinfo)
        if courses.exists():
            return render(request,self.template_name,{'form':self.form_class,'error':error,'pic':currentuserinfo,'courses':courses})
        else:
            return render(request,self.template_name,{'form':self.form_class,'error':error,'pic':currentuserinfo})

    def post(self,request,error=None):
        user_info_form_data = self.form_class(request.POST,request.FILES)
        if user_info_form_data.is_valid():
            save_user_name(user_info_form_data.cleaned_data,request.user.username)
            if user:=Teacher.objects.get(user=request.user):
                update_user_information(user_info_form_data.cleaned_data,user)
            else:
                user_info_form_data.save()
            return redirect(self.success_url)
        else:
            error_msg_dict = json.loads(user_info_form_data.errors.as_json())
            if error_msg_dict['phone']:
                error_msg = error_msg_dict['phone'][0]['message']
            else:
                error_msg = error_msg_dict['__all__'][0]['message']
            return redirect('teacher_dashboard_error',error_msg)
        
class TeacherContact(StudentContact):
    template_name = 'teach_contact.html'
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