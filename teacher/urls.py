from django.urls import path
from .views import TeacherDashboard,TeacherContact

urlpatterns = [
    path('teacher/dashboard/',TeacherDashboard.as_view(),name='teacher_dashboard'),
    path('teacher/dashboard/<str:error>',TeacherDashboard.as_view(),name='teacher_dashboard_error'),
    path('teacher/contact',TeacherContact.as_view(),name='teacher_contact')
]
