from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name=''),
    path('login', views.login, name='login'),
    path('blank', views.blank, name='blank'),
    path('404', views.pg_404, name='404'),
    
    # Urls Teachers
    path('teacher', views.teacher, name='teacher'),
    path('teacher/add', views.add_teacher, name='add_teacher'),
    path('teacher/edit/<int:pk>', views.edit_teacher, name='edit_teacher'),
    path('teacher/del/<int:pk>', views.del_teacher, name='del_teacher'),

    # Urls Students
    path('student', views.student, name='student'),
    path('student/add', views.add_student, name='add_student'),
    path('student/edit/<int:pk>', views.edit_student, name='edit_student'),
    path('student/del/<int:pk>', views.del_student, name='del_student'),

    # Urls Courses
    path('course', views.course, name='course'),
    path('course/add', views.add_course, name='add_course'),
    path('course/edit/<int:pk>', views.edit_course, name='edit_course'),
    path('course/del/<int:pk>', views.del_course, name='del_course'),

    # Urls Levels
    path('level', views.level, name='level'),
    path('level/add', views.add_level, name='add_level'),
    path('level/edit/<int:pk>', views.edit_level, name='edit_level'),
    path('level/del/<int:pk>', views.del_level, name='del_level'),

    # Urls Positions
    path('position', views.position, name='position'),
    path('position/add', views.add_position, name='add_position'),
    path('position/edit/<int:pk>', views.edit_position, name='edit_position'),
    path('position/del/<int:pk>', views.del_position, name='del_position'),

    # Urls Times
    path('time', views.time, name='time'),
    path('time/add', views.add_time, name='add_time'),
    path('time/edit/<int:pk>', views.edit_time, name='edit_time'),
    path('time/del/<int:pk>', views.del_time, name='del_time'),

    # Urls Sessions
    path('session', views.session, name='session'),
    path('session/add', views.add_session, name='add_session'),
    path('session/edit/<int:pk>', views.edit_session, name='edit_session'),
    path('session/del/<int:pk>', views.del_session, name='del_session'),

    # Urls Sessions_Class
    path('session_student', views.session_student, name='session_student'),
    path('session_student/add', views.add_session_student, name='add_session_student'),
    path('session_student/edit/<int:pk>', views.edit_session_student, name='edit_session_student'),
    path('session_student/del/<int:pk>', views.del_session_student, name='del_session_student'),

]