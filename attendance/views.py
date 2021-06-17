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

from home.views import update_attendance
from course.views import get_request_session_course_id

# Create your views here.

@login_required(login_url='login')
def select_attendance(request):
    get_course_id = get_request_session_course_id(request)
    course = Course.objects.all()
    if request.method =='POST':
        get_type = request.POST['type']
        request.session['attendance_type'] = get_type
        if get_type=='1':
            return redirect('attendance_teacher')
        else:
            return redirect('attendance_student')
    context = {'course': course,
                
                }
    return render(request, 'attendance/attendance_select_course.html', context)

@login_required(login_url='login')
def attendance_generater(request):
    get_course_id = get_request_session_course_id(request)
    # Get data from form
    get_sdate = get_course_id.start_date
    get_num = get_course_id.num_of_session
    new_date = []
    for i in range(get_num):
        new_date.append(get_sdate)
        get_sdate = get_sdate + timedelta(days=7)
    # Get course id
    session = Session.objects.filter(course_id=get_course_id)
    session_list = session.values_list('session_id', flat=True)
    # Check if teacher or student are in attendance
    person_in_attandance = Attendance.objects.filter(session_id__in=session_list).values_list('person_id' ,flat=True)
    ###
    #person_list = Person.objects.all().values_list('person_id' ,flat=True)
    teacher = session.filter(~Q(teacher_id_id=None)).filter(~Q(teacher_id__in=person_in_attandance)).values_list('teacher_id', flat=True)
    session_student = Session_Student.objects.filter(session_id__in=session_list)
    student = session_student.filter(~Q(student_id__in=person_in_attandance)).values_list('student_id', flat=True)
    ###
    # Add teacher to attendance
    for item in teacher:
        get_teacher = Person.objects.get(pk=item)
        get_session = session.get(teacher_id=get_teacher)
        count_index = Attendance.objects.all().count()
        if count_index == 0:
            count_index = 1
        else:
            count_index = Attendance.objects.all().aggregate(Max('attendance_id'))['attendance_id__max']
            count_index += 1
        for x in range(get_num):
            Attendance.objects.create(attendance_id=count_index, person_id=get_teacher, session_id=get_session, day=new_date[x], status=False)
            count_index += 1
    # Add student to attendance
    for item in student:
        get_student = Person.objects.get(pk=item)
        get_session_student = session_student.get(student_id=get_student)
        count_index = Attendance.objects.all().count()
        if count_index == 0:
            count_index = 1
        else:
            count_index = Attendance.objects.all().aggregate(Max('attendance_id'))['attendance_id__max']
            count_index += 1
        for x in range(get_num):
            Attendance.objects.create(attendance_id=count_index, person_id=get_student, session_id=get_session_student.session_id, day=new_date[x], status=False)
            count_index += 1
    messages.success(request, 'تم الانشاء بنجاح')
    return HttpResponseRedirect(reverse('attendance'))

@login_required(login_url='login')
def attendance_teacher(request):
    get_course_id = get_request_session_course_id(request)
    # Get all teachers
    session = Session.objects.filter(course_id=get_course_id)
    teacher = session.values_list('teacher_id', flat=True)
    session_list = session.values_list('session_id', flat=True)
    day_attendance = Attendance.objects.all().filter(person_id__in=teacher, session_id__in=session_list).values_list('day', flat=True).order_by('day').distinct()
    get_attendance = Attendance.objects.all().filter(person_id__in=teacher, session_id__in=session_list).distinct('person_id')
    attendance = []
    for all_person in get_attendance:
        status_attendance = Attendance.objects.all().filter(person_id=all_person.person_id, session_id__in=session_list).values_list('status', flat=True).order_by('day')
        id_attendance = Attendance.objects.all().filter(person_id=all_person.person_id, session_id__in=session_list).values_list('attendance_id', flat=True).order_by('day')
        zip_id_day = zip(status_attendance, id_attendance)
        dic_attendance = {'person_id': all_person.person_id, 'session_number': all_person.session_id.session_number , 'first_name': all_person.person_id.first_name, 'last_name': all_person.person_id.last_name, 'zip_id_day': zip_id_day}
        attendance.append(dic_attendance)
    context = {'day_attendance': day_attendance,
                'attendance': attendance,
                }
    return render(request, 'attendance/attendance_teacher.html', context)

@login_required(login_url='login')
def attendance_student(request):
    get_course_id = get_request_session_course_id(request)
    # Get all teachers
    session = Session.objects.all().filter(course_id=get_course_id)
    session_list = session.values_list('session_id', flat=True)
    student = Session_Student.objects.filter(session_id__in=session_list).values_list('student_id', flat=True)
    day_attendance = Attendance.objects.all().filter(person_id__in=student, session_id__in=session_list).values_list('day', flat=True).order_by('day').distinct()
    get_attendance = Attendance.objects.all().filter(person_id__in=student, session_id__in=session_list).distinct('person_id')
    attendance = []
    for all_person in get_attendance:
        status_attendance = Attendance.objects.all().filter(person_id=all_person.person_id, session_id__in=session_list).values_list('status', flat=True).order_by('day')
        id_attendance = Attendance.objects.all().filter(person_id=all_person.person_id, session_id__in=session_list).values_list('attendance_id', flat=True).order_by('day')
        zip_id_day = zip(status_attendance, id_attendance)
        dic_attendance = {'person_id': all_person.person_id, 'session_number': all_person.session_id.session_number , 'first_name': all_person.person_id.first_name, 'last_name': all_person.person_id.last_name, 'zip_id_day': zip_id_day}
        attendance.append(dic_attendance)
    context = {'day_attendance': day_attendance,
                'attendance': attendance,
                }
    return render(request, 'attendance/attendance_student.html', context)

def change_status_true(request):   
    attendance_id = request.GET.get('attendance_id')
    attendance = Attendance.objects.get(pk=attendance_id)
    attendance.status = True
    attendance.save()
    context = {}
    return JsonResponse(context)

def change_status_false(request):   
    attendance_id = request.GET.get('attendance_id')
    attendance = Attendance.objects.get(pk=attendance_id)
    attendance.status = False
    attendance.save()
    context = {}
    return JsonResponse(context)


def export_excel_attendance(request):    
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="attendance.xls"'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Students')
    # Sheet header, first row
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    ###
    get_course_id = get_request_session_course_id(request)
    session_list = Session.objects.filter(course_id=get_course_id).values_list('session_id', flat=True)
    day_attendance = Attendance.objects.all().filter(session_id__in=session_list).order_by('day').distinct('day')
    columns = ['id', 'First name', 'Last name', 'BDate', 'Phone number', 'Type', 'Priority', 'Session', 'Level']
    for day in day_attendance:
        get_day = day.day
        get_day = get_day.strftime('%m/%d/%Y')
        columns.append(get_day)
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)
    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()
    rows = []
    ###
    get_attendance = Attendance.objects.all().filter(session_id__in=session_list).distinct('person_id')
    for all_person in get_attendance:
        status_attendance = Attendance.objects.all().filter(person_id=all_person.person_id, session_id__in=session_list).order_by('day')
        id = ''
        fname = ''
        lname = ''
        bdate = ''
        phone_number = ''
        type_person= ''
        priority = ''
        session = ''
        level = ''
        # Check all values if none
        if all_person.person_id.person_id is not None:
            id = all_person.person_id.person_id
        if all_person.person_id.first_name is not None:
            fname = all_person.person_id.first_name
        if all_person.person_id.last_name is not None:
            lname = all_person.person_id.last_name
        if all_person.person_id.bdate is not None:
            bdate = all_person.person_id.bdate
            bdate = bdate.strftime('%Y')
        if all_person.person_id.phone_number is not None:
            phone_number = all_person.person_id.phone_number    
        if all_person.person_id.type_id is not None:
            type_person = all_person.person_id.type_id
        if all_person.person_id.priority_id is not None:
            priority = all_person.person_id.priority_id
        if all_person.session_id.session_number is not None:
            session = all_person.session_id.session_number
        if all_person.session_id.level_id is not None:
            level = str(all_person.session_id.level_id)
        # Enter values
        value = [id, fname, lname, bdate, phone_number, type_person, priority, session, level]
        for st in status_attendance:
            status = str(False)
            if st.status is not None:
                status = str(st.status)
            value.append(status)
        rows.append(value)
    ###        
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)
    wb.save(response)
    return response