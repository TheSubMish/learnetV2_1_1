from .forms import UserInformationForm,UserPreferenceForm
from teacher.forms import TeacherInformationForm
from .models import Student,UserPreference
from userlog.models import CustomUser
import json

def get_user_information(currentuser,currentuserinfo):
    if currentuser.role:
        userform = TeacherInformationForm(initial={
            'first_name': currentuser.first_name,
            'last_name': currentuser.last_name,
            'profilepic': currentuserinfo.profilepic,
            'phone': currentuserinfo.phone,
            'city': currentuserinfo.city,
            'district': currentuserinfo.district,
            'state': currentuserinfo.state,
            'edubackground': currentuserinfo.edubackground,
            'teachexp': currentuserinfo.teachexp
        })
    else:
        userform = UserInformationForm(initial={
            'first_name': currentuser.first_name,
            'last_name': currentuser.last_name,
            'profilepic': currentuserinfo.profilepic,
            'phone': currentuserinfo.phone,
            'city': currentuserinfo.city,
            'district': currentuserinfo.district,
            'state': currentuserinfo.state,
            'edubackground': currentuserinfo.edubackground
        })
    return userform

def get_user_preferences(request):
    try:
        currentuserinfo = Student.objects.get(user=request.user)
        currentuserpref = UserPreference.objects.get(user=currentuserinfo)
    except UserPreference.DoesNotExist:
        return None
    
    prefform = UserPreferenceForm(initial={
        'html': currentuserpref.html,
        'css': currentuserpref.css,
        'javascript': currentuserpref.javascript,
        'python': currentuserpref.python,
        'data_analysis': currentuserpref.data_analysis,
        'data_structure_and_algorithms': currentuserpref.data_structure_and_algorithms,
        'natural_language_processing': currentuserpref.natural_language_processing,
        'machine_learning': currentuserpref.machine_learning
    })

    return prefform

def save_user_name(form_data,username):
    first_name = form_data.get('first_name')
    last_name = form_data.get('last_name')
    currentuser = CustomUser.objects.get(username=username)
    currentuser.first_name = first_name
    currentuser.last_name = last_name
    currentuser.save()
    return

def update_user_information(form_data,user):
    user.profilepic = form_data.get('profilepic')
    user.phone = form_data.get('phone')
    user.city = form_data.get('city')
    user.district = form_data.get('district')
    user.state = form_data.get('state')
    user.edubackground = form_data.get('edubackground')
    try:
        user.teachexp = form_data.get('teachexp')
    except Exception:
        pass
    user.save()
    return

def user_info_function(request,user_info_form_data):
        if user_info_form_data.is_valid():
            save_user_name(user_info_form_data.cleaned_data,request.user.username)
            if user:=Student.objects.get(user=request.user):
                update_user_information(user_info_form_data.cleaned_data,user)
            else:
                user_info_form_data.save()
            return True
        else:
            error_msg_dict = json.loads(user_info_form_data.errors.as_json())
            if error_msg_dict['phone']:
                error_msg = error_msg_dict['phone'][0]['message']
            else:
                error_msg = error_msg_dict['__all__'][0]['message']
            return error_msg

def update_pref(form_data,prefUser):
    prefUser.html = form_data.get('html')
    prefUser.css = form_data.get('css')
    prefUser.javascript = form_data.get('javascript')
    prefUser.python = form_data.get('python')
    prefUser.data_analysis = form_data.get('data_analysis')
    prefUser.data_structure_and_algorithms = form_data.get('data_structure_and_algorithms')
    prefUser.natural_language_processing = form_data.get('natural_language_processing')
    prefUser.machine_learning = form_data.get('machine_learning')
    prefUser.save()
    return

def create_pref(form_data,user):
    UserPreference.objects.create(
        user = user,
        html = form_data.get('html'),
        css = form_data.get('css'),
        javascript = form_data.get('javascript'),
        python = form_data.get('python'),
        data_analysis = form_data.get('data_analysis'),
        data_structure_and_algorithms = form_data.get('data_structure_and_algorithms'),
        natural_language_processing = form_data.get('natural_language_processing'),
        machine_learning = form_data.get('machine_learning')
    )
    return