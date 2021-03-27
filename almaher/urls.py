from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name=''),
    path('login', views.login, name='login'),
    path('blank', views.blank, name='blank'),
    path('404', views.pg_404, name='404'),
    
    path('teacher', views.teacher, name='teacher'),
    path('teacher/add', views.add_teacher, name='add_teacher'),
    path('teacher/edit/<int:pk>', views.edit_teacher, name='edit_teacher'),
    path('teacher/del/<int:pk>', views.del_teacher, name='del_teacher'),

    path('student', views.student, name='student'),
    path('student/add', views.add_student, name='add_student'),
    path('student/edit/<int:pk>', views.edit_student, name='edit_student'),
    path('student/del/<int:pk>', views.del_student, name='del_student'),

]