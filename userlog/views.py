from django.shortcuts import render,redirect
from django.views.generic.base import TemplateView,RedirectView
from django.views.generic.edit import CreateView,FormView
from django.urls import reverse_lazy
from django.contrib.auth import login,logout
from django.contrib.auth import authenticate
import json

from .forms import CustomUserForm,LogInForm
from .models import CustomUser
from .validation import signValidate,emailPasswordValidate
from student.models import Student
from teacher.models import Teacher

class IndexPage(TemplateView):
    template_name = 'index.html'

class SignUpPage(CreateView):
    template_name = 'signup.html'
    model = CustomUser
    form_class = CustomUserForm
    
    def post(self, request, *args, **kwargs):
        form_data = self.form_class(request.POST)
        if form_data.is_valid():
            if error_msg:=signValidate(form_data.cleaned_data):
                return render(request, self.template_name, {"form": form_data,'error': error_msg})
            print(form_data.cleaned_data)
            user = form_data.save()
            login(request,user)
            role = form_data.cleaned_data['role']
            newUser = CustomUser.objects.get(username=form_data.cleaned_data['username'])
            if role:
                Teacher.objects.create(user=newUser)
                return redirect('teacher_dashboard')
            else:
                Student.objects.create(user=newUser)
                return redirect('student_dashboard')
        else:
            error_msg = emailPasswordValidate(form_data.errors.as_json())
            return render(request, self.template_name, {"form": form_data,'error': error_msg})

class LogInPage(FormView):
    form_class = LogInForm
    template_name = 'login.html'
    success_url = reverse_lazy('home')

    def post(self, request, *args, **kwargs):
        form_data = self.form_class(request.POST)
        if form_data.is_valid():
            username = form_data.cleaned_data['username']
            password = form_data.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                next_url = request.GET.get('next')
                if next_url:
                    return redirect(next_url)
                return redirect(self.success_url)
        else:
            error_msg_dict = json.loads(form_data.errors.as_json())
            error_msg = error_msg_dict['__all__'][0]['message']
            return render(request,self.template_name,{'form':self.form_class, 'error':error_msg})

def logoutPage(request):
    logout(request)
    # Get the previous page URL from the request headers
    previous_page = request.META.get('HTTP_REFERER', '/')
    return redirect(previous_page)

class RedirectDashboard(RedirectView):
    
    def get_redirect_url(self,*args,**kwargs):
        user = self.request.user
        try:
            Student.objects.get(user=user)
            return '/student/dashboard/'
        except Student.DoesNotExist:
            Teacher.objects.get(user=user)
            return '/teacher/dashboard/'
        except Teacher.DoesNotExist:
            return '/login/'