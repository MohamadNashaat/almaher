from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import *

# Create your views here.

#@login_required(login_url='login')
def index(request):
    c_teacher = Person.objects.all().filter(type_id=1).count()
    c_student = Person.objects.all().filter(type_id=2).count()
    c_course = Course.objects.all().count()
    c_session = Session.objects.all().count()
    context = {'c_teacher': c_teacher, 
                'c_student': c_student,
                'c_session': c_session,
                'c_course': c_course}
    return render(request, 'almaher/index.html', context)

def login(request):
    return render(request, 'almaher/login.html')

def blank(request):
    return render(request, 'almaher/blank.html')

def pg_404(request):
    return render(request, 'almaher/404.html')

# Views Teachers
def teacher(request):
    teacher = Person.objects.all().filter(type_id=1)
    c_teacher = teacher.count()
    context = {'c_teacher': c_teacher,
                'teacher': teacher}
    return render(request, 'almaher/teacher.html', context)

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
        new_teacher = Person(type_id=p_type, first_name=fname, last_name=lname,
                            father_name=father_n, home_number=hn, phone_number=pn,
                            job=j, address=ad, bdate=bd)
        new_teacher.save()
        messages.success(request, 'Add success!')
        return HttpResponseRedirect(reverse('teacher'))
    
    return render(request, 'almaher/add_teacher.html')

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

def del_teacher(request, pk):
    teacher = Person.objects.get(person_id=pk)
    if request.method =='POST':
        teacher.delete()
        return redirect('teacher')
    return render(request, 'almaher/del_teacher.html', {'teacher': teacher})
    
# Views Students
def student(request):
    student = Person.objects.all().filter(type_id=2)
    c_student = student.count()
    context = {'c_student': c_student,
                'student': student}
    return render(request, 'almaher/student.html', context)

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
            new_teacher = Person(type_id=p_type, first_name=fname, last_name=lname,
                            father_name=father_n, home_number=hn, phone_number=pn,
                            job=j, address=ad, bdate=bd, level_id=get_level)
        else:
            new_teacher = Person(type_id=p_type, first_name=fname, last_name=lname,
                            father_name=father_n, home_number=hn, phone_number=pn,
                            job=j, address=ad, bdate=bd)              
        new_teacher.save()
        messages.success(request, 'Add success!')
        return HttpResponseRedirect(reverse('student'))
    context = {'level': level}
    return render(request, 'almaher/add_student.html', context)

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

def del_student(request, pk):
    student = Person.objects.get(person_id=pk)
    if request.method =='POST':
        student.delete()
        return redirect('student')
    return render(request, 'almaher/del_student.html', {'student': student})

# Views Course
def course(request):
    course = Course.objects.all()
    context = {'course': course}
    return render(request, 'almaher/course.html', context)

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

def edit_course(request):
    pass

def del_course(request, pk):
    get_course = Course.objects.get(pk=pk)
    get_course.delete()
    return redirect('course')

# Views Level
def level(request):
    level = Level.objects.all()
    context = {'level': level}
    return render(request, 'almaher/level.html', context)

def add_level(request):
    if request.method == 'POST':
        nlevel = request.POST['nlevel']
        new_level = Level(level_name=nlevel)            
        new_level.save()
        messages.success(request, 'Add success!')
        return HttpResponseRedirect(reverse('level'))
    return render(request, 'almaher/add_level.html')

def edit_level(request):
    pass

def del_level(request, pk):
    get_level = Level.objects.get(pk=pk)
    get_level.delete()
    return redirect('level')

# Views Position
def position(request):
    position = Position.objects.all()
    context = {'position': position}
    return render(request, 'almaher/position.html', context)

def add_position(request):
    if request.method == 'POST':
        nposition = request.POST['nposition']
        new_position = Position(position_name=nposition)            
        new_position.save()
        messages.success(request, 'Add success!')
        return HttpResponseRedirect(reverse('position'))
    return render(request, 'almaher/add_position.html')

def edit_position(request):
    pass

def del_position(request, pk):
    get_position = Position.objects.get(pk=pk)
    get_position.delete()
    return redirect('position')

# Views Time
def time(request):
    time = Time.objects.all()
    context = {'time': time}
    return render(request, 'almaher/time.html', context)

def add_time(request):
    if request.method == 'POST':
        ntime = request.POST['ntime']
        new_time = Time(time_name=ntime)            
        new_time.save()
        messages.success(request, 'Add success!')
        return HttpResponseRedirect(reverse('time'))
    return render(request, 'almaher/add_time.html')

def edit_time(request):
    pass

def del_time(request, pk):
    get_time = Time.objects.get(pk=pk)
    get_time.delete()
    return redirect('time')

# Views Session
def session(request):
    session = Session.objects.all()
    context = {'session': session}
    return render(request, 'almaher/session.html', context)

def add_session(request):
    course = Course.objects.all()
    level = Level.objects.all()
    position = Position.objects.all()
    time = Time.objects.all()
    teacher = Person.objects.all().filter(type_id=1)
    student = Person.objects.all().filter(type_id=2)
    if request.method == 'POST':
        snumber = request.POST['snumber']
        course = Course.objects.get(pk=request.POST['course'])
        teacher = Person.objects.get(pk=request.POST['teacher'])
        level = Level.objects.get(pk=request.POST['level'])
        position = Position.objects.get(pk=request.POST['position'])
        time = Time.objects.get(pk=request.POST['time'])
        new_session = Session(level_id=level, course_id=course,
                             position_id=position, time_id=time, session_number=snumber, teacher_id=teacher)
        new_session.save()
        messages.success(request, 'Add success!')
        return HttpResponseRedirect(reverse('session'))
    context = {'course': course,
                'level': level,
                'position': position,
                'time': time,
                'teacher': teacher,
                'student': student,
                }
    return render(request, 'almaher/add_session.html', context)

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

    teacher = Person.objects.all().filter(type_id=1)
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

def del_session(request, pk):
    get_session = Session.objects.get(pk=pk)
    get_session.delete()
    return redirect('session')

# Views Session_Student
def session_student(request, pk):
    session = Session.objects.get(session_id=pk)
    session_student = Session_Student.objects.all().filter(session_id=pk)
    in_session = Session_Student.objects.all().filter(session_id=pk).values_list('student_id', flat=True)
    in_session = list(in_session)
    # Q objects can be negated with the ~ operator
    all_student = Person.objects.all().filter(~Q(pk__in=in_session)).filter(type_id=2, level_id=session.level_id)
    student = all_student
    context = {'session': session,
                'session_student': session_student,
                'student': student}
    return render(request, 'almaher/session_student.html', context)

def add_session_student(request, pk, num):
    session = Session.objects.get(pk=pk)
    student = Person.objects.get(pk=num)
    add_new = Session_Student(session_id=session, student_id=student)
    add_new.save()
    return redirect('session_student', pk)

def del_session_student(request, pk, num):
    get_session_student = Session_Student.objects.get(pk=num)
    get_session_student.delete()
    return redirect('session_student', pk)