from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name=''),
    path('login', views.user_login, name='login'),
     path('logout', views.user_logout, name='logout'),
    path('blank', views.blank, name='blank'),
    path('404', views.pg_404, name='404'),
    
    # Manage Person
    path('person', views.person, name='person'),
    path('person/edit/<int:pk>', views.edit_person, name='edit_person'),
    path('person/del/<int:pk>', views.del_person, name='del_person'),
    path('person/lock/<int:pk>', views.lock_person, name='lock_person'),
    path('person/unlock/<int:pk>', views.unlock_person, name='unlock_person'),
    path('graduate', views.graduate, name='graduate'),
    path('wait/list', views.wait_list, name='wait_list'),
    # Urls Teachers
    path('teacher', views.teacher, name='teacher'),
    path('teacher/add', views.add_teacher, name='add_teacher'),
    # Urls Students
    path('student', views.student, name='student'),
    path('student/add', views.add_student, name='add_student'),

    # Urls Courses
    path('course', views.course, name='course'),
    path('select/course', views.select_course, name='select_course'),
    path('course/add', views.add_course, name='add_course'),
    path('course/del/<int:pk>', views.del_course, name='del_course'),    

    # Urls Sessions
    path('session', views.session, name='session'),
    path('session/generate', views.generate_session, name='generate_session'),
    path('session/add', views.add_session, name='add_session'),
    path('session/edit/<int:pk>', views.edit_session, name='edit_session'),
    path('session/del/<int:pk>', views.del_session, name='del_session'),
    # Urls Sessions_Students
    path('session/student/<int:pk>', views.session_student, name='session_student'),
    path('session/student/add/<int:pk>/<int:num>', views.add_session_student, name='add_session_student'),
    path('session/student/del/<int:pk>/<int:num>', views.del_session_student, name='del_session_student'),
    path('view/session/student', views.view_session_student, name='view_session_student'),
    path('session/wait/list', views.wait_list_session, name='wait_list_session'),

    # Urls Attendance
    path('select/attendance', views.select_attendance, name='attendance'),
    path('attendance/teacher', views.attendance_teacher, name='attendance_teacher'),
    path('attendance/student', views.attendance_student, name='attendance_student'),
    path('attendance/generater', views.attendance_generater, name='attendance_generater'),
    
    # JSON
    path('ajax/change_status_true', views.change_status_true, name='change_status_true'),
    path('ajax/change_status_false', views.change_status_false, name='change_status_false'),
    path('ajax/set_teacher', views.set_teacher, name='set_teacher'),
    path('ajax/set_student', views.set_student, name='set_student'),
    path('ajax/set_priority', views.set_priority, name='set_priority'),
    path('ajax/set_exam_mark', views.set_exam_mark, name='set_exam_mark'),

    # Urls Exam
    path('exam', views.exam, name='exam'),
    path('exam/generate', views.generate_exam, name='generate_exam'),

    # Urls Result
    path('result', views.result, name='result'),
    path('result/generate', views.generate_result, name='generate_result'),   

    # Urls Export to *
    path('export/excel/student', views.export_excel_student, name='export_excel_student'),
    path('export/excel/teacher', views.export_excel_teacher, name='export_excel_teacher'),
    path('export/pdf/session', views.export_session_pdf, name='export_session_pdf'),
    path('export/excel/attendance/student', views.export_excel_attendance_student, name='export_excel_attendance_student'),
    path('export/excel/attendance/teacher', views.export_excel_attendance_teacher, name='export_excel_attendance_teacher'),
    
]