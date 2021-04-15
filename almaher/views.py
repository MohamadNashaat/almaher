from .models import *
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth import authenticate ,login, logout
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta
from django.db.models import Q
import xlwt

# Create your views here.

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
    return render(request, 'almaher/login.html')

def user_logout(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def blank(request):
    return render(request, 'almaher/blank.html')

@login_required(login_url='login')
def pg_404(request):
    return render(request, 'almaher/404.html')

@login_required(login_url='login')
def index(request):
    c_teacher = Person.objects.all().filter(person_type_id=1).count()
    c_student = Person.objects.all().filter(person_type_id=2).count()
    c_course = Course.objects.all().count()
    c_session = Session.objects.all().count()
    context = {'c_teacher': c_teacher, 
                'c_student': c_student,
                'c_session': c_session,
                'c_course': c_course}
    return render(request, 'almaher/index.html', context)

# Views Teachers
@login_required(login_url='login')
def teacher(request):
    teacher = Person.objects.all().filter(person_type_id=1)
    c_teacher = teacher.count()
    context = {'c_teacher': c_teacher,
                'teacher': teacher}
    return render(request, 'almaher/teacher.html', context)

@login_required(login_url='login')
def add_teacher(request):
    if request.method == 'POST':
        fname = request.POST['fname']
        lname = request.POST['lname']
        father_n = request.POST['father_name']
        j = request.POST['job']
        pn = request.POST['pnumber']
        hn = request.POST['hnumber']
        ad = request.POST['address']
        bd = request.POST['bdate']
        p_type = Person_Type.objects.get(pk=1)
        new_teacher = Person(person_type_id=p_type, first_name=fname, last_name=lname,
                            father_name=father_n, home_number=hn, phone_number=pn,
                            job=j, address=ad, bdate=bd)
        new_teacher.save()
        messages.success(request, 'Add success!')
        return HttpResponseRedirect(reverse('teacher'))
    
    return render(request, 'almaher/add_teacher.html')

@login_required(login_url='login')
def edit_teacher(request, pk):
    teacher = Person.objects.get(person_id=pk)
    if request.method =='POST':
        fname = request.POST['fname']
        lname = request.POST['lname']
        father_n = request.POST['father_name']
        j = request.POST['job']
        pn = request.POST['pnumber']
        hn = request.POST['hnumber']
        ad = request.POST['address']
        bd = request.POST['bdate']
        teacher.first_name = fname
        teacher.last_name = lname
        teacher.father_name = father_n
        teacher.job = j
        teacher.phone_number = pn
        teacher.home_number = hn
        teacher.address = ad
        teacher.bdate = bd
        teacher.save()
        return redirect('teacher')
    return render(request, 'almaher/edit_teacher.html', {'teacher': teacher})

@login_required(login_url='login')
def del_teacher(request, pk):
    teacher = Person.objects.get(person_id=pk)
    if request.method =='POST':
        teacher.delete()
        return redirect('teacher')
    return render(request, 'almaher/del_teacher.html', {'teacher': teacher})
    
# Views Students
@login_required(login_url='login')
def student(request):
    student = Person.objects.all().filter(person_type_id=2)
    c_student = student.count()
    context = {'c_student': c_student,
                'student': student}
    return render(request, 'almaher/student.html', context)

@login_required(login_url='login')
def add_student(request):
    level = Level.objects.all()
    if request.method == 'POST':
        fname = request.POST['fname']
        lname = request.POST['lname']
        father_n = request.POST['father_name']
        j = request.POST['job']
        pn = request.POST['pnumber']
        hn = request.POST['hnumber']
        ad = request.POST['address']
        bd = request.POST['bdate']
        p_type = Person_Type.objects.get(pk=2)
        level_id = request.POST['level']
        if level_id != 0:
            get_level = Level.objects.get(pk=level_id)
            new_teacher = Person(person_type_id=p_type, first_name=fname, last_name=lname,
                            father_name=father_n, home_number=hn, phone_number=pn,
                            job=j, address=ad, bdate=bd, level_id=get_level)
        else:
            new_teacher = Person(person_type_id=p_type, first_name=fname, last_name=lname,
                            father_name=father_n, home_number=hn, phone_number=pn,
                            job=j, address=ad, bdate=bd)              
        new_teacher.save()
        messages.success(request, 'Add success!')
        return HttpResponseRedirect(reverse('student'))
    context = {'level': level}
    return render(request, 'almaher/add_student.html', context)

@login_required(login_url='login')
def edit_student(request, pk):
    student = Person.objects.get(person_id=pk)
    level = Level.objects.all()
    if request.method =='POST':
        fname = request.POST['fname']
        lname = request.POST['lname']
        father_n = request.POST['father_name']
        j = request.POST['job']
        pn = request.POST['pnumber']
        hn = request.POST['hnumber']
        ad = request.POST['address']
        bd = request.POST['bdate']
        student.first_name = fname
        student.last_name = lname
        student.father_name = father_n
        student.job = j
        student.phone_number = pn
        student.home_number = hn
        student.address = ad
        student.bdate = bd
        level_id = request.POST['level']
        if level_id != 0:
            level = Level.objects.get(pk=level_id)
            student.level_id = level
        student.save()
        return redirect('student')
    context = {'student': student,
                'level': level}
    return render(request, 'almaher/edit_student.html', context)

@login_required(login_url='login')
def del_student(request, pk):
    student = Person.objects.get(person_id=pk)
    if request.method =='POST':
        student.delete()
        return redirect('student')
    return render(request, 'almaher/del_student.html', {'student': student})

# Views Course
@login_required(login_url='login')
def course(request):
    course = Course.objects.all()
    context = {'course': course}
    return render(request, 'almaher/course.html', context)

@login_required(login_url='login')
def add_course(request):
    if request.method == 'POST':
        ncourse = request.POST['ncourse']
        sdate = request.POST['sdate']
        edate = request.POST['edate']
        new_ncourse = Course(course_name=ncourse, start_date=sdate, end_date=edate)
        new_ncourse.save()
        messages.success(request, 'Add success!')
        return HttpResponseRedirect(reverse('course'))
    return render(request, 'almaher/add_course.html')

@login_required(login_url='login')
def del_course(request, pk):
    get_course = Course.objects.get(pk=pk)
    get_course.delete()
    return redirect('course')

# Views Level
@login_required(login_url='login')
def level(request):
    level = Level.objects.all()
    context = {'level': level}
    return render(request, 'almaher/level.html', context)

@login_required(login_url='login')
def add_level(request):
    if request.method == 'POST':
        nlevel = request.POST['nlevel']
        new_level = Level(level_name=nlevel)            
        new_level.save()
        messages.success(request, 'Add success!')
        return HttpResponseRedirect(reverse('level'))
    return render(request, 'almaher/add_level.html')

@login_required(login_url='login')
def del_level(request, pk):
    get_level = Level.objects.get(pk=pk)
    get_level.delete()
    return redirect('level')

# Views Position
@login_required(login_url='login')
def position(request):
    position = Position.objects.all()
    context = {'position': position}
    return render(request, 'almaher/position.html', context)

@login_required(login_url='login')
def add_position(request):
    if request.method == 'POST':
        nposition = request.POST['nposition']
        new_position = Position(position_name=nposition)            
        new_position.save()
        messages.success(request, 'Add success!')
        return HttpResponseRedirect(reverse('position'))
    return render(request, 'almaher/add_position.html')

@login_required(login_url='login')
def del_position(request, pk):
    get_position = Position.objects.get(pk=pk)
    get_position.delete()
    return redirect('position')

# Views Time
@login_required(login_url='login')
def time(request):
    time = Time.objects.all()
    context = {'time': time}
    return render(request, 'almaher/time.html', context)

@login_required(login_url='login')
def add_time(request):
    if request.method == 'POST':
        ntime = request.POST['ntime']
        new_time = Time(time_name=ntime)            
        new_time.save()
        messages.success(request, 'Add success!')
        return HttpResponseRedirect(reverse('time'))
    return render(request, 'almaher/add_time.html')

@login_required(login_url='login')
def del_time(request, pk):
    get_time = Time.objects.get(pk=pk)
    get_time.delete()
    return redirect('time')

# Views Session

@login_required(login_url='login')
def session(request):    
    get_course_id = request.session['get_course_id']
    session = Session.objects.all().filter(course_id=get_course_id)
    context = {'session': session,
                'get_course_id': get_course_id
                }
    return render(request, 'almaher/session.html', context)

@login_required(login_url='login')
def add_session(request):
    get_course_id = request.session['get_course_id']
    get_course_id = Course.objects.get(pk=get_course_id)
    level = Level.objects.all()
    position = Position.objects.all()
    time = Time.objects.all()
    in_session = Session.objects.all().filter(course_id=get_course_id).values_list('teacher_id', flat=True)
    teacher = Person.objects.all().filter(person_type_id=1).filter(~Q(pk__in=in_session))
    if request.method == 'POST':
        snumber = request.POST['snumber']
        teacher = Person.objects.get(pk=request.POST['teacher'])
        level = Level.objects.get(pk=request.POST['level'])
        position = Position.objects.get(pk=request.POST['position'])
        time = Time.objects.get(pk=request.POST['time'])
        new_session = Session(level_id=level, course_id=get_course_id,
                             position_id=position, time_id=time, session_number=snumber, teacher_id=teacher)
        new_session.save()
        messages.success(request, 'Add success!')
        return HttpResponseRedirect(reverse('session'))
    context = {'level': level,
                'position': position,
                'time': time,
                'teacher': teacher,
                }
    return render(request, 'almaher/add_session.html', context)

@login_required(login_url='login')
def edit_session(request, pk):
    session = Session.objects.get(pk=pk)
    if request.method =='POST':
        get_snumber = request.POST['snumber']
        get_course = request.POST['course']
        get_teacher = request.POST['teacher']
        get_level = request.POST['level']
        get_position = request.POST['position']
        get_time = request.POST['time']
        #
        course = Course.objects.get(pk=get_course)
        teacher = Person.objects.get(pk=get_teacher)
        level = Level.objects.get(pk=get_level)
        position = Position.objects.get(pk=get_position)
        time = Time.objects.get(pk=get_time)
        #
        session.session_number = get_snumber
        session.course_id = course
        session.teacher_id = teacher
        session.level_id = level
        session.time_id = time
        session.save()
        messages.success(request, 'Edit success!')
        return HttpResponseRedirect(reverse('session'))

    get_course_id = request.session['get_course_id']
    get_course_id = Course.objects.get(pk=get_course_id)
    in_session = Session.objects.all().filter(course_id=get_course_id).filter(~Q(teacher_id=session.teacher_id)).values_list('teacher_id', flat=True)
    teacher = Person.objects.all().filter(person_type_id=1).filter(~Q(pk__in=in_session))
    position = Position.objects.all()
    level = Level.objects.all()
    time = Time.objects.all()
    course = Course.objects.all()
    context = {'session': session,
                'teacher': teacher,
                'position': position,
                'level': level,
                'time': time,
                'course': course
                }
    return render(request, 'almaher/edit_session.html', context)

@login_required(login_url='login')
def del_session(request, pk):
    get_session = Session.objects.get(pk=pk)
    get_session.delete()
    return redirect('session')

# Views Session_Student
@login_required(login_url='login')
def session_student(request, pk):
    session = Session.objects.get(session_id=pk)
    session_student = Session_Student.objects.all().filter(session_id=pk)
    # Get student not Enrolment in sessions
    get_course_id = request.session['get_course_id']
    get_course_id = Course.objects.get(pk=get_course_id)
    get_session = Session.objects.all().filter(course_id=get_course_id).values_list('session_id', flat=True)
    in_session = Session_Student.objects.all().filter(session_id__in=get_session).filter().values_list('student_id', flat=True)
    # Q objects can be negated with the ~ operator
    all_student = Person.objects.all().filter(~Q(pk__in=in_session)).filter(person_type_id=2, level_id=session.level_id)
    student = all_student
    context = {'session': session,
                'session_student': session_student,
                'student': student}
    return render(request, 'almaher/session_student.html', context)

@login_required(login_url='login')
def add_session_student(request, pk, num):
    session = Session.objects.get(pk=pk)
    student = Person.objects.get(pk=num)
    add_new = Session_Student(session_id=session, student_id=student)
    add_new.save()
    return redirect('session_student', pk)

@login_required(login_url='login')
def del_session_student(request, pk, num):
    get_session_student = Session_Student.objects.get(pk=num)
    get_session_student.delete()
    return redirect('session_student', pk)

# Views select course
@login_required(login_url='login')
def select_course(request):
    course = Course.objects.all()
    if request.method =='POST':
        get_course = request.POST['course']
        get_course = Course.objects.get(pk=get_course)
        # Set session course_id
        request.session['get_course_id'] = get_course.course_id
        return redirect('session')
    context = {'course': course,
                }
    return render(request, 'almaher/select_course.html', context)

# View view_sessions
@login_required(login_url='login')
def view_select_course(request):
    course = Course.objects.all()
    if request.method =='POST':
        get_course = request.POST['course']
        get_course = Course.objects.get(pk=get_course)
        # Set session course_id
        request.session['get_course_id'] = get_course.course_id
        return redirect('view_session_student')
    context = {'course': course,
                }
    return render(request, 'almaher/view_select_course.html', context)

@login_required(login_url='login')
def view_session_student(request):
    get_course_id = request.session['get_course_id']
    get_course_id = Course.objects.get(pk=get_course_id)
    session = Session.objects.all().filter(course_id=get_course_id).values_list('session_id', flat=True)
    session_student = Session_Student.objects.all().filter(session_id__in=session)
    context = {'session_student': session_student,
                }
    return render(request, 'almaher/view_session_student.html', context)

# View attendance
@login_required(login_url='login')
def select_attendance(request):
    course = Course.objects.all()
    if request.method =='POST':
        get_type = request.POST['type']
        request.session['attendance_type'] = get_type
        get_course = request.POST['course']
        get_course = Course.objects.get(pk=get_course)
        request.session['get_course_id'] = get_course.course_id
        if get_type=='1':
            return redirect('attendance_teacher')
        else:
            return redirect('attendance_student')
    context = {'course': course,
                }
    return render(request, 'almaher/attendance_select_course.html', context)

@login_required(login_url='login')
def attendance_teacher(request):
    teacher = Person.objects.all().filter(person_type_id=1).values_list('person_id', flat=True)
    get_course_id = request.session['get_course_id']
    session = Session.objects.all().filter(course_id=get_course_id).values_list('session_id', flat=True)
    name_attendance = Attendance.objects.all().filter(person_id__in=teacher, session_id__in=session).distinct('person_id')
    day_attendance = Attendance.objects.all().filter(person_id__in=teacher, session_id__in=session).values_list('day', flat=True).order_by('day').distinct()
    status_attendance = Attendance.objects.all().filter(person_id__in=teacher, session_id__in=session).order_by('day')
    context = {'name_attendance': name_attendance,
                'day_attendance': day_attendance,
                'status_attendance': status_attendance,
                }
    return render(request, 'almaher/attendance_teacher.html', context)

@login_required(login_url='login')
def attendance_student(request):
    student = Person.objects.all().filter(person_type_id=2).values_list('person_id', flat=True)
    get_course_id = request.session['get_course_id']
    session = Session.objects.all().filter(course_id=get_course_id).values_list('session_id', flat=True)
    name_attendance = Attendance.objects.all().filter(person_id__in=student, session_id__in=session).distinct('person_id')
    day_attendance = Attendance.objects.all().filter(person_id__in=student, session_id__in=session).values_list('day', flat=True).order_by('day').distinct()
    status_attendance = Attendance.objects.all().filter(person_id__in=student, session_id__in=session).order_by('day')
    context = {'name_attendance': name_attendance,
                'day_attendance': day_attendance,
                'status_attendance': status_attendance,
                }
    return render(request, 'almaher/attendance_student.html', context)

def change_status_true(request):   
    attendance_id = request.GET.get('attendance_id')
    attendance = Attendance.objects.get(pk=attendance_id)
    attendance.status = True
    attendance.save()
    context = {        
    }
    return JsonResponse(context)

def change_status_false(request):   
    attendance_id = request.GET.get('attendance_id')
    attendance = Attendance.objects.get(pk=attendance_id)
    attendance.status = False
    attendance.save()
    context = {        
    }
    return JsonResponse(context)

@login_required(login_url='login')
def attendance_generater(request):
    course = Course.objects.all()
    if request.method =='POST':
        get_course = request.POST['course']
        # Get start date and number for loop
        get_sdate = request.POST['sdate']
        get_sdate = datetime.strptime(get_sdate, "%Y-%m-%d")
        get_num = int(request.POST['num'])
        new_date = []
        for i in range(get_num):
            new_date.append(get_sdate)
            get_sdate = get_sdate + timedelta(days=7)
        # Get course id
        get_course = Course.objects.get(pk=get_course)
        session = Session.objects.all().filter(course_id=get_course)
        session_list = session.values_list('session_id', flat=True)
        teacher = session.values_list('teacher_id', flat=True)
        session_student = Session_Student.objects.all().filter(session_id__in=session_list)
        student = session_student.values_list('student_id', flat=True)
        
        # Add teacher to attendance
        for item in teacher:
            get_teacher = Person.objects.get(pk=item)
            get_session = session.get(teacher_id=get_teacher)
            for x in range(get_num):
                Attendance.objects.create(person_id=get_teacher, session_id=get_session, day=new_date[x], status=False)

        # Add student to attendance
        for item in student:
            get_student = Person.objects.get(pk=item)
            get_session_student = session_student.get(student_id=get_student) 
            for x in range(get_num):
                Attendance.objects.create(person_id=get_student, session_id=get_session_student.session_id, day=new_date[x], status=False)
        
        messages.success(request, 'Add success!')
        return HttpResponseRedirect(reverse('attendance'))
    context = {'course': course,
                }
    return render(request, 'almaher/attendance_generater.html', context)

# View exam
@login_required(login_url='login')
def select_exam(request):
    course = Course.objects.all()
    exam_time = Exam_Time.objects.all()
    if request.method =='POST':
        get_course = request.POST['course']
        get_course = Course.objects.get(pk=get_course)
        request.session['get_course_id'] = get_course.course_id
        get_exam_time = request.POST['exam_time']
        get_exam_time = Exam_Time.objects.get(pk=get_exam_time)
        request.session['get_exam_time'] = get_exam_time.exam_time_id
        return redirect('exam')
    context = {'course': course,
                'exam_time': exam_time,
                }
    return render(request, 'almaher/exam_select_course.html', context)

@login_required(login_url='login')
def exam(request):
    get_course_id = request.session['get_course_id']
    get_course_id = Course.objects.get(pk=get_course_id)
    #get_exam_time = request.session['get_exam_time']
    #get_exam = Exam_Time.objects.get(pk=get_exam_time)
    #session = Session.objects.filter(course_id=get_course_id)
    #in_session = session.values_list('session_id', float=True)
    #exam = Exam.objects.filter(session_id__in=in_session, exam_time_id=get_exam.exam_time_id)
    #context = {'exam': exam,
    #            }
    return render(request, 'almaher/exam.html')


# Export to *
def export_excel_student(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="students.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Students')

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['Person id', 'First name', 'Last name', 'Father name', 'Home number',
                'Phone number', 'Level_id', 'Birth date', 'Job', 'Address']

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    rows = []

    persons = Person.objects.all().filter(person_type_id=2)
    
    for person in persons:
        person_bd = person.bdate
        person_bd = person_bd.strftime('%m/%d/%Y')
        vlues = [person.person_id, person.first_name, person.last_name, person.father_name, 
            person.home_number, person.phone_number, person.level_id.level_name, person_bd,
            person.job, person.address]
        rows.append(vlues)

    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)
    return response

def export_excel_teacher(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="teacher.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Students')

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['Person id', 'First name', 'Last name', 'Father name', 'Home number',
                'Phone number', 'Birth date', 'Job', 'Address']

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    rows = []

    persons = Person.objects.all().filter(person_type_id=1)
    
    for person in persons:
        person_bd = person.bdate
        person_bd = person_bd.strftime('%m/%d/%Y')
        vlues = [person.person_id, person.first_name, person.last_name, person.father_name, 
            person.home_number, person.phone_number, person_bd,
            person.job, person.address]
        rows.append(vlues)

    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)
    return response

def export_excel_attendance_student(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="attendance_student.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Students')

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    student = Person.objects.all().filter(person_type_id=2).values_list('person_id', flat=True)
    get_course_id = request.session['get_course_id']
    session = Session.objects.all().filter(course_id=get_course_id).values_list('session_id', flat=True)
    day_attendance = Attendance.objects.all().filter(person_id__in=student, session_id__in=session).order_by('day').distinct('day')

    columns = ['Session number', 'First name', 'Last name']

    for day in day_attendance:
        get_day = day.day
        get_day = get_day.strftime('%m/%d/%Y')
        columns.append(get_day)

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    rows = []

    name_attendance = Attendance.objects.all().filter(person_id__in=student, session_id__in=session).distinct('person_id')
    status_attendance = Attendance.objects.all().filter(person_id__in=student, session_id__in=session).order_by('day')
        
    for attendance in name_attendance:
        value = [attendance.session_id.session_number, attendance.person_id.first_name, attendance.person_id.last_name]
        for s_attendance in status_attendance:
            if attendance.person_id == s_attendance.person_id:
                value.append(str(s_attendance.status))
        rows.append(value)

    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)
    return response



def export_excel_attendance_teacher(request):    
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="attendance_teacher.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Students')

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    teacher = Person.objects.all().filter(person_type_id=1).values_list('person_id', flat=True)
    get_course_id = request.session['get_course_id']
    session = Session.objects.all().filter(course_id=get_course_id).values_list('session_id', flat=True)
    day_attendance = Attendance.objects.all().filter(person_id__in=teacher, session_id__in=session).order_by('day').distinct('day')
    columns = ['Session number', 'First name', 'Last name']

    for day in day_attendance:
        get_day = day.day
        get_day = get_day.strftime('%m/%d/%Y')
        columns.append(get_day)

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    rows = []

    name_attendance = Attendance.objects.all().filter(person_id__in=teacher, session_id__in=session).distinct('person_id')
    status_attendance = Attendance.objects.all().filter(person_id__in=teacher, session_id__in=session).order_by('day')
    
    for attendance in name_attendance:
        value = [attendance.session_id.session_number, attendance.person_id.first_name, attendance.person_id.last_name]
        for s_attendance in status_attendance:
            if attendance.person_id == s_attendance.person_id:
                value.append(str(s_attendance.status))
        rows.append(value)

    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)
    return response