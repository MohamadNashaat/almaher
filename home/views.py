from .models import *
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth import authenticate ,login, logout
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta
from django.db.models import Max
from django.db.models import Q
import xlwt
import tempfile
from django.template.loader import render_to_string
from weasyprint import HTML
from weasyprint.fonts import FontConfiguration
# Import models
from course.models import Course
from level.models import Level
from period.models import Time
from position.models import Position
from person.models import Person
from session.models import Session, Session_Student
from exam.models import Exam
from result.models import Result
from attendance.models import Attendance

# Create your views here.

# Login
def user_login(request):
    if request.user.is_authenticated:
        return redirect('')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('')
            else:
                messages.info(request, 'Please enter the correct username and password!')
    return render(request, 'home/login.html')

# Logout
def user_logout(request):
    logout(request)
    return redirect('login')

# Blank
@login_required(login_url='login')
def blank(request):
    return render(request, 'home/blank.html')

# Page 404
@login_required(login_url='login')
def pg_404(request):
    return render(request, 'home/404.html')

# Index
@login_required(login_url='login')
def index(request):
    # Check request session
    if not request.session.get('get_course_id', False):
        return redirect('select_course')
    get_course_id = request.session['get_course_id']
    get_course_id = Course.objects.get(pk=get_course_id)

    c_teacher = Person.objects.all().filter(type_id='Teacher').count()
    c_student = Person.objects.all().filter(type_id='Student').count()
    c_graduate = Person.objects.all().filter(type_id='Graduate').count()
    c_course = Course.objects.all().count()
    session = Session.objects.filter(course_id=get_course_id)
    c_session = session.count()
    c_session_student = Session_Student.objects.filter(session_id__in=session).count()

    #level = Level.objects.all()
    #student_count = []
    #teacher_count = []
    #level_list = level.values_list('level_name', flat=True)
    #for level_loop in level_list:
    #    s_count = Person.objects.filter(type_id='Student' ,level_id=level_loop).count()
    #    t_count = Person.objects.filter(type_id__in=('Teacher', 'Graduate') ,level_id=level_loop, status=True).count()
    #    student_count.append(s_count)
    #    teacher_count.append(t_count)
    #zip_list = zip(level_list, student_count)
    #zip_list2 = zip(level_list, teacher_count)

    context = {'c_teacher': c_teacher,
                'c_student': c_student,
                'c_graduate': c_graduate,
                'c_course': c_course,
                'c_session': c_session,
                'c_session_student': c_session_student,
                'get_course_id': get_course_id,            
                #'zip_list': zip_list,
                #'zip_list2': zip_list2,
                }
    return render(request, 'home/index.html', context)