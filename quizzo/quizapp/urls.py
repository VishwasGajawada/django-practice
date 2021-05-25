from django.urls import path
from django.contrib.auth.views import LoginView,LogoutView
from . import views
urlpatterns = [
    path('',views.index,name='index'),
    path('login/',LoginView.as_view(template_name='registration/login.html'),name='login'),
    path('logout/',LogoutView.as_view(),name='logout'),
    path('signup/',views.signup,name='signup'),
    path('student_signup/',views.student_signup,name='student_signup'),
    path('teacher_signup/',views.teacher_signup,name='teacher_signup'),
    path('subject/<slug:subject_slug>/',views.show_subject,name='subject'),
    path('subject/<slug:subject_slug>/grades/',views.subject_grades,name='subject_grades'),
    path('subject/<slug:subject_slug>/people/',views.subject_people,name='subject_people'),
    path('subject/<slug:subject_slug>/quiz/<str:pk>/',views.quiz_detail,name='quiz_detail'),
    path('subject_add/',views.add_subject,name='add_subject'),
    path('create_subject/',views.create_subject,name='create_subject'),
    path('profile/',views.profile,name='profile'),
    path('mark_answer/<str:pk>/',views.mark_answer,name='mark_answer'),
]
