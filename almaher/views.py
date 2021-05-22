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
    return render(request, 'almaher/login.html')

# Logout
def user_logout(request):
    logout(request)
    return redirect('login')

# Blank
@login_required(login_url='login')
def blank(request):
    return render(request, 'almaher/blank.html')

# Page 404
@login_required(login_url='login')
def pg_404(request):
    return render(request, 'almaher/404.html')

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
    c_session = Session.objects.filter(course_id=get_course_id).count()

    level = Level.objects.all()
    student_count = []
    teacher_count = []
    level_list = level.values_list('level_name', flat=True)
    for level_loop in level_list:
        s_count = Person.objects.filter(type_id='Student' ,level_id=level_loop).count()
        t_count = Person.objects.filter(type_id__in=('Teacher', 'Graduate') ,level_id=level_loop, status=True).count()
        student_count.append(s_count)
        teacher_count.append(t_count)
    zip_list = zip(level_list, student_count)
    zip_list2 = zip(level_list, teacher_count)

    context = {'c_teacher': c_teacher, 
                'c_student': c_student,
                'c_graduate': c_graduate,
                'c_course': c_course,
                'c_session': c_session,
                'get_course_id': get_course_id,
                'zip_list': zip_list,
                'zip_list2': zip_list2,
                }
    return render(request, 'almaher/index.html', context)

# Manage Person
@login_required(login_url='login')
def person(request):
    person = Person.objects.all()
    context = {'person': person,
                }
    return render(request, 'almaher/person.html', context)

@login_required(login_url='login')
def edit_person(request, pk):
    level = Level.objects.all()
    person = Person.objects.get(person_id=pk)
    if request.method =='POST':
        fname = request.POST['fname']
        lname = request.POST['lname']
        father_n = request.POST['father_name']
        j = request.POST['job']
        pn = request.POST['pnumber']
        hn = request.POST['hnumber']
        ad = request.POST['address']
        bd = request.POST['bdate']
        level = request.POST['level']
        level = Level.objects.get(pk=level)
        person.first_name = fname
        person.last_name = lname
        person.father_name = father_n
        person.job = j
        person.phone_number = pn
        person.home_number = hn
        person.address = ad
        person.bdate = bd
        person.level_id = level
        person.save()
        return redirect('person')
    context = {'person': person,
                'level': level,
                }
    return render(request, 'almaher/edit_person.html', context)

@login_required(login_url='login')
def del_person(request, pk):
    person = Person.objects.get(person_id=pk)
    if request.method =='POST':
        person.delete()
        return redirect('person')
    context = {'person': person,
                }
    return render(request, 'almaher/del_person.html', context)

# Wait List
@login_required(login_url='login')
def wait_list(request):
    person = Person.objects.all().filter(status=False)
    context = {'person': person,
                }
    return render(request, 'almaher/wait_list.html', context)

# Lock & Unlock Person
@login_required(login_url='login')
def lock_person(request, pk):
    person = Person.objects.get(person_id=pk)
    person.status = False
    person.save()
    if(person.type_id == 'Teacher'):
        return redirect('teacher')
    elif(person.type_id == 'Student'):
        return redirect('student')
    else:
        return redirect('graduate')

@login_required(login_url='login')
def unlock_person(request, pk):
    person = Person.objects.get(person_id=pk)
    person.status = True
    person.save()
    return redirect('wait_list')

# Manage Graduate
@login_required(login_url='login')
def graduate(request):
    graduate = Person.objects.all().filter(type_id='Graduate')
    context = {'graduate': graduate,
                }
    return render(request, 'almaher/graduate.html', context)

# Views Teachers
@login_required(login_url='login')
def teacher(request):
    teacher = Person.objects.all().filter(type_id='Teacher', status=True)
    c_teacher = teacher.count()
    context = {'c_teacher': c_teacher,
                'teacher': teacher,
                }
    return render(request, 'almaher/teacher.html', context)

@login_required(login_url='login')
def add_teacher(request):
    level = Level.objects.all()
    if request.method == 'POST':
        # Get index id
        count_index = Person.objects.all().count()
        if count_index == 0:
            count_index = 1
        else:
            count_index = Person.objects.all().aggregate(Max('person_id'))['person_id__max']
            count_index += 1
        fname = request.POST['fname']
        lname = request.POST['lname']
        father_n = request.POST['father_name']
        j = request.POST['job']
        pn = request.POST['pnumber']
        hn = request.POST['hnumber']
        ad = request.POST['address']
        bd = request.POST['bdate']
        level = request.POST['level']
        level = Level.objects.get(pk=level)
        Person.objects.create(person_id=count_index, type_id='Teacher', first_name=fname, last_name=lname,
                            father_name=father_n, home_number=hn, phone_number=pn,
                            job=j, address=ad, bdate=bd, level_id=level)
        messages.success(request, 'تم الاضافة بنجاح')
        return HttpResponseRedirect(reverse('add_teacher'))
    context = {'level': level,
                }
    return render(request, 'almaher/add_teacher.html', context)

# Views Students
@login_required(login_url='login')
def student(request):
    student = Person.objects.all().filter(type_id='Student', status=True)
    context = {'student': student,
                }
    return render(request, 'almaher/student.html', context)

@login_required(login_url='login')
def add_student(request):
    level = Level.objects.all()
    if request.method == 'POST':
        count_index = Person.objects.all().count()
        if count_index == 0:
            count_index = 1
        else:
            count_index = Person.objects.all().aggregate(Max('person_id'))['person_id__max']
            count_index += 1
        fname = request.POST['fname']
        lname = request.POST['lname']
        father_n = request.POST['father_name']
        j = request.POST['job']
        pn = request.POST['pnumber']
        hn = request.POST['hnumber']
        ad = request.POST['address']
        bd = request.POST['bdate']
        level = request.POST['level']
        priority = request.POST['priority']
        level = Level.objects.get(pk=level)
        Person.objects.create(person_id=count_index, type_id='Student', first_name=fname, last_name=lname,
                        father_name=father_n, home_number=hn, phone_number=pn,
                        job=j, address=ad, bdate=bd, level_id=level, priority_id=priority)
        messages.success(request, 'تم الاضافة بنجاح')
        return HttpResponseRedirect(reverse('add_student'))
    context = {'level': level,
                }
    return render(request, 'almaher/add_student.html', context)

# Views select course
@login_required(login_url='login')
def select_course(request):
    # Check if course equal zero
    ch_course = Course.objects.count()
    if ch_course < 1:
        return redirect('add_course')
    elif request.method == 'POST':
        get_course = request.POST['course']
        get_course = Course.objects.get(pk=get_course)
        # Set session course_id
        request.session['get_course_id'] = get_course.course_id
        return redirect('')
    course = Course.objects.all().order_by('pk')
    context = {'course': course,
                }
    return render(request, 'almaher/select_course.html', context)

# Views Course
@login_required(login_url='login')
def course(request):
    course = Course.objects.all()
    context = {'course': course,
                }
    return render(request, 'almaher/course.html', context)

@login_required(login_url='login')
def add_course(request):
    if request.method == 'POST':
        count_index = Course.objects.all().count()
        if count_index == 0:
            count_index = 1
        else:
            count_index = Course.objects.all().aggregate(Max('course_id'))['course_id__max']
            count_index += 1
        ncourse = request.POST['ncourse']
        sdate = request.POST['sdate']
        edate = request.POST['edate']
        count_of_session = request.POST['count_of_session']
        Course.objects.create(course_id=count_index, 
                                course_name=ncourse, 
                                start_date=sdate, 
                                end_date=edate,
                                num_of_session=count_of_session)
        messages.success(request, 'تم الاضافة بنجاح')
        return HttpResponseRedirect(reverse('course'))
    context = {}
    return render(request, 'almaher/add_course.html', context)

@login_required(login_url='login')
def del_course(request, pk):
    get_course = Course.objects.get(pk=pk)
    get_course.delete()
    return redirect('course')

# Views Session
@login_required(login_url='login')
def session(request):
    # Check request session
    if not request.session.get('get_course_id', False):
        return redirect('select_course')
    get_course_id = request.session['get_course_id']
    get_course_id = Course.objects.get(pk=get_course_id)

    session = Session.objects.all().filter(course_id=get_course_id)
    session_list_students = session.values_list('session_id', flat=True)
    session_list = session.filter(~Q(teacher_id=None)).values_list('session_id', flat=True)
    in_session_teacher = Session.objects.all().filter(pk__in=session_list).values_list('teacher_id', flat=True)
    teacher = Person.objects.filter(type_id__in=('Teacher', 'Graduate'), status=True).filter(~Q(pk__in=in_session_teacher)).order_by('first_name')
    end_session = []
    for s_loop in session_list_students:
            get_session = Session.objects.all().get(pk=s_loop)
            c_student = Session_Student.objects.filter(session_id=get_session).count()
            dic_session = {
                'session_id': get_session.session_id,
                'session_number': get_session.session_number,
                'course_id': get_session.course_id,
                'level_id': get_session.level_id,
                'position_id': get_session.position_id,
                'time_id': get_session.time_id,
                'teacher_id': get_session.teacher_id,
                'count': c_student,}
            end_session.append(dic_session)
    context = {'end_session': end_session,
                'teacher': teacher,
                }
    return render(request, 'almaher/session.html', context)

@login_required(login_url='login')
def generate_session(request):
    # Check request session
    if not request.session.get('get_course_id', False):
        return redirect('select_course')
    get_course_id = request.session['get_course_id']
    get_course_id = Course.objects.get(pk=get_course_id)            

    level = Level.objects.all()
    student_count = []
    level_list = level.values_list('level_name', flat=True)
    for level_loop in level_list:
        l_count = Person.objects.filter(type_id='Student' ,level_id=level_loop).count()
        student_count.append(l_count)
    zip_list = zip(level_list, student_count)

    if request.method == 'POST':
        # Get index id session
        count_index = Session.objects.all().count()
        if count_index == 0:
            count_index = 1
        else:
            count_index = Session.objects.all().aggregate(Max('session_id'))['session_id__max']
            count_index += 1
        # Get index id session student
        count_index_s_student = Session_Student.objects.all().count()
        if count_index_s_student == 0:
            count_index_s_student = 1
        else:
            count_index_s_student = Session_Student.objects.all().aggregate(Max('id'))['id__max']
            count_index_s_student += 1

        ch_session = Session.objects.filter(course_id=get_course_id).count()
        if ch_session == 0:
            # Times
            time = Time.objects.get(pk='بعد جلسة الصفا')
            # Levels
            advanced_b = Level.objects.get(pk='متقدم ب')
            advanced_a = Level.objects.get(pk='متقدم أ')
            intermediate_b = Level.objects.get(pk='متوسط ب')
            intermediate_a = Level.objects.get(pk='متوسط أ')
            beginner_b = Level.objects.get(pk='مبتدئ ب')
            beginner_a = Level.objects.get(pk='مبتدئ أ')
            # Get request
            count_student_1 = int(request.POST.get('count_student_1'))
            count_student_1 += 1
            count_student_2 = int(request.POST.get('count_student_2'))
            count_student_2 += 1
            #
            count_advanced_b = int(request.POST.get('متقدم ب'))
            count_advanced_a = int(request.POST.get('متقدم أ'))
            count_intermediate_b = int(request.POST.get('متوسط ب'))
            count_intermediate_a = int(request.POST.get('متوسط أ'))
            count_beginner_b = int(request.POST.get('مبتدئ ب'))
            count_beginner_a = int(request.POST.get('مبتدئ أ'))
            # Add number 1
            count_advanced_b += 1
            count_advanced_a += count_advanced_b
            count_intermediate_b += count_advanced_a
            count_intermediate_a += count_intermediate_b
            count_beginner_b += count_intermediate_a
            count_beginner_a += count_beginner_b
            # Positions
            p1 = Position.objects.get(pk='توسعة مكتبة')
            p2 = Position.objects.get(pk='قبو')
            p3 = Position.objects.get(pk='توسعة حرم رئيسي')
            p4 = Position.objects.get(pk='حرم رئيسي')
            p5 = Position.objects.get(pk='تحت السدة')
            # Loop to create sessons
            for l1 in range(1, count_advanced_b):
                new_session = Session(session_id=count_index, level_id=advanced_b,course_id=get_course_id,session_number=l1, time_id=time, position_id=p1)
                new_session.save()
                count_index += 1
                # Add students => "مستمر" to sessions
                get_session = Session.objects.all().filter(course_id=get_course_id).values_list('session_id', flat=True)
                in_session = Session_Student.objects.all().filter(session_id__in=get_session).values_list('student_id', flat=True)
                student = Person.objects.filter(~Q(pk__in=in_session)).filter(type_id='Student', status=True, level_id=new_session.level_id, priority_id="مستمر").order_by('bdate').values_list('person_id', flat=True)
                var_num = 0
                for s_loop in range(1, count_student_1): 
                    if var_num < len(student):
                        get_student = int(student[var_num])
                        new_student = Person.objects.get(pk=get_student)
                        Session_Student.objects.create(id=count_index_s_student, session_id=new_session, student_id=new_student)
                        var_num += 1
                        count_index_s_student += 1
                    else:
                        break
                # Add students => "غير معروف" to sessions
                get_session = Session.objects.all().filter(course_id=get_course_id).values_list('session_id', flat=True)
                in_session = Session_Student.objects.all().filter(session_id__in=get_session).values_list('student_id', flat=True)
                student = Person.objects.filter(~Q(pk__in=in_session)).filter(type_id='Student', status=True, level_id=new_session.level_id, priority_id="غير معروف").order_by('bdate').values_list('person_id', flat=True)
                var_num = 0
                for s_loop in range(1, count_student_2): 
                    if var_num < len(student):
                        get_student = int(student[var_num])
                        new_student = Person.objects.get(pk=get_student)
                        Session_Student.objects.create(id=count_index_s_student, session_id=new_session, student_id=new_student)
                        var_num += 1
                        count_index_s_student += 1
                    else:
                        break

            for l1 in range(count_advanced_b, count_advanced_a):
                new_session = Session(session_id=count_index, level_id=advanced_a,course_id=get_course_id,session_number=l1, time_id=time, position_id=p2)
                new_session.save()
                count_index += 1
                # Add students => "مستمر" to sessions
                get_session = Session.objects.all().filter(course_id=get_course_id).values_list('session_id', flat=True)
                in_session = Session_Student.objects.all().filter(session_id__in=get_session).values_list('student_id', flat=True)
                student = Person.objects.filter(~Q(pk__in=in_session)).filter(type_id='Student', status=True, level_id=new_session.level_id, priority_id="مستمر").order_by('bdate').values_list('person_id', flat=True)
                var_num = 0
                for s_loop in range(1, count_student_1): 
                    if var_num < len(student):
                        get_student = int(student[var_num])
                        new_student = Person.objects.get(pk=get_student)
                        Session_Student.objects.create(id=count_index_s_student, session_id=new_session, student_id=new_student)
                        var_num += 1
                        count_index_s_student += 1
                    else:
                        break
                # Add students => "غير معروف" to sessions
                get_session = Session.objects.all().filter(course_id=get_course_id).values_list('session_id', flat=True)
                in_session = Session_Student.objects.all().filter(session_id__in=get_session).values_list('student_id', flat=True)
                student = Person.objects.filter(~Q(pk__in=in_session)).filter(type_id='Student', status=True, level_id=new_session.level_id, priority_id="غير معروف").order_by('bdate').values_list('person_id', flat=True)
                var_num = 0
                for s_loop in range(1, count_student_2): 
                    if var_num < len(student):
                        get_student = int(student[var_num])
                        new_student = Person.objects.get(pk=get_student)
                        Session_Student.objects.create(id=count_index_s_student, session_id=new_session, student_id=new_student)
                        var_num += 1
                        count_index_s_student += 1
                    else:
                        break

            for l1 in range(count_advanced_a, count_intermediate_b):
                new_session = Session(session_id=count_index, level_id=intermediate_b,course_id=get_course_id,session_number=l1, time_id=time, position_id=p3)
                new_session.save()
                count_index += 1
                # Add students => "مستمر" to sessions
                get_session = Session.objects.all().filter(course_id=get_course_id).values_list('session_id', flat=True)
                in_session = Session_Student.objects.all().filter(session_id__in=get_session).values_list('student_id', flat=True)
                student = Person.objects.filter(~Q(pk__in=in_session)).filter(type_id='Student', status=True, level_id=new_session.level_id, priority_id="مستمر").order_by('bdate').values_list('person_id', flat=True)
                var_num = 0
                for s_loop in range(1, count_student_1): 
                    if var_num < len(student):
                        get_student = int(student[var_num])
                        new_student = Person.objects.get(pk=get_student)
                        Session_Student.objects.create(id=count_index_s_student, session_id=new_session, student_id=new_student)
                        var_num += 1
                        count_index_s_student += 1
                    else:
                        break
                # Add students => "غير معروف" to sessions
                get_session = Session.objects.all().filter(course_id=get_course_id).values_list('session_id', flat=True)
                in_session = Session_Student.objects.all().filter(session_id__in=get_session).values_list('student_id', flat=True)
                student = Person.objects.filter(~Q(pk__in=in_session)).filter(type_id='Student', status=True, level_id=new_session.level_id, priority_id="غير معروف").order_by('bdate').values_list('person_id', flat=True)
                var_num = 0
                for s_loop in range(1, count_student_2): 
                    if var_num < len(student):
                        get_student = int(student[var_num])
                        new_student = Person.objects.get(pk=get_student)
                        Session_Student.objects.create(id=count_index_s_student, session_id=new_session, student_id=new_student)
                        var_num += 1
                        count_index_s_student += 1
                    else:
                        break

            for l1 in range(count_intermediate_b, count_intermediate_a):
                new_session = Session(session_id=count_index, level_id=intermediate_a,course_id=get_course_id,session_number=l1, time_id=time, position_id=p4)
                new_session.save()
                count_index += 1
                # Add students => "مستمر" to sessions
                get_session = Session.objects.all().filter(course_id=get_course_id).values_list('session_id', flat=True)
                in_session = Session_Student.objects.all().filter(session_id__in=get_session).values_list('student_id', flat=True)
                student = Person.objects.filter(~Q(pk__in=in_session)).filter(type_id='Student', status=True, level_id=new_session.level_id, priority_id="مستمر").order_by('bdate').values_list('person_id', flat=True)
                var_num = 0
                for s_loop in range(1, count_student_1): 
                    if var_num < len(student):
                        get_student = int(student[var_num])
                        new_student = Person.objects.get(pk=get_student)
                        Session_Student.objects.create(id=count_index_s_student, session_id=new_session, student_id=new_student)
                        var_num += 1
                        count_index_s_student += 1
                    else:
                        break
                # Add students => "غير معروف" to sessions
                get_session = Session.objects.all().filter(course_id=get_course_id).values_list('session_id', flat=True)
                in_session = Session_Student.objects.all().filter(session_id__in=get_session).values_list('student_id', flat=True)
                student = Person.objects.filter(~Q(pk__in=in_session)).filter(type_id='Student', status=True, level_id=new_session.level_id, priority_id="غير معروف").order_by('bdate').values_list('person_id', flat=True)
                var_num = 0
                for s_loop in range(1, count_student_2): 
                    if var_num < len(student):
                        get_student = int(student[var_num])
                        new_student = Person.objects.get(pk=get_student)
                        Session_Student.objects.create(id=count_index_s_student, session_id=new_session, student_id=new_student)
                        var_num += 1
                        count_index_s_student += 1
                    else:
                        break

            for l1 in range(count_intermediate_a, count_beginner_b):
                new_session = Session(session_id=count_index, level_id=beginner_b,course_id=get_course_id,session_number=l1, time_id=time, position_id=p5)
                new_session.save()
                count_index += 1
                # Add students => "مستمر" to sessions
                get_session = Session.objects.all().filter(course_id=get_course_id).values_list('session_id', flat=True)
                in_session = Session_Student.objects.all().filter(session_id__in=get_session).values_list('student_id', flat=True)
                student = Person.objects.filter(~Q(pk__in=in_session)).filter(type_id='Student', status=True, level_id=new_session.level_id, priority_id="مستمر").order_by('bdate').values_list('person_id', flat=True)
                var_num = 0
                for s_loop in range(1, count_student_1): 
                    if var_num < len(student):
                        get_student = int(student[var_num])
                        new_student = Person.objects.get(pk=get_student)
                        Session_Student.objects.create(id=count_index_s_student, session_id=new_session, student_id=new_student)
                        var_num += 1
                        count_index_s_student += 1
                    else:
                        break
                # Add students => "غير معروف" to sessions
                get_session = Session.objects.all().filter(course_id=get_course_id).values_list('session_id', flat=True)
                in_session = Session_Student.objects.all().filter(session_id__in=get_session).values_list('student_id', flat=True)
                student = Person.objects.filter(~Q(pk__in=in_session)).filter(type_id='Student', status=True, level_id=new_session.level_id, priority_id="غير معروف").order_by('bdate').values_list('person_id', flat=True)
                var_num = 0
                for s_loop in range(1, count_student_2): 
                    if var_num < len(student):
                        get_student = int(student[var_num])
                        new_student = Person.objects.get(pk=get_student)
                        Session_Student.objects.create(id=count_index_s_student, session_id=new_session, student_id=new_student)
                        var_num += 1
                        count_index_s_student += 1
                    else:
                        break

            for l1 in range(count_beginner_b, count_beginner_a):
                new_session = Session(session_id=count_index, level_id=beginner_a,course_id=get_course_id,session_number=l1, time_id=time, position_id=p1)
                new_session.save()
                count_index += 1
                # Add students => "مستمر" to sessions
                get_session = Session.objects.all().filter(course_id=get_course_id).values_list('session_id', flat=True)
                in_session = Session_Student.objects.all().filter(session_id__in=get_session).values_list('student_id', flat=True)
                student = Person.objects.filter(~Q(pk__in=in_session)).filter(type_id='Student', status=True, level_id=new_session.level_id, priority_id="مستمر").order_by('bdate').values_list('person_id', flat=True)
                var_num = 0
                for s_loop in range(1, count_student_1): 
                    if var_num < len(student):
                        get_student = int(student[var_num])
                        new_student = Person.objects.get(pk=get_student)
                        Session_Student.objects.create(id=count_index_s_student, session_id=new_session, student_id=new_student)
                        var_num += 1
                        count_index_s_student += 1
                    else:
                        break
                # Add students => "غير معروف" to sessions
                get_session = Session.objects.all().filter(course_id=get_course_id).values_list('session_id', flat=True)
                in_session = Session_Student.objects.all().filter(session_id__in=get_session).values_list('student_id', flat=True)
                student = Person.objects.filter(~Q(pk__in=in_session)).filter(type_id='Student', status=True, level_id=new_session.level_id, priority_id="غير معروف").order_by('bdate').values_list('person_id', flat=True)
                var_num = 0
                for s_loop in range(1, count_student_2): 
                    if var_num < len(student):
                        get_student = int(student[var_num])
                        new_student = Person.objects.get(pk=get_student)
                        Session_Student.objects.create(id=count_index_s_student, session_id=new_session, student_id=new_student)
                        var_num += 1
                        count_index_s_student += 1
                    else:
                        break

        return redirect('session')
    context = {'level': level,
                'zip_list': zip_list,
                }
    return render(request, 'almaher/generate_session.html', context)


@login_required(login_url='login')
def add_session(request):
    # Check request session
    if not request.session.get('get_course_id', False):
        return redirect('select_course')
    get_course_id = request.session['get_course_id']
    get_course_id = Course.objects.get(pk=get_course_id)

    count_index = Session.objects.all().count()
    if count_index == 0:
        count_index = 1
    else:
        count_index = Session.objects.all().aggregate(Max('session_id'))['session_id__max']
        count_index += 1
    in_session = Session.objects.all().filter(course_id=get_course_id).values_list('teacher_id', flat=True)
    teacher = Person.objects.all().filter(type_id__in=('Teacher', 'Graduate'))
    teacher = teacher.filter(~Q(pk__in=in_session))
    if request.method == 'POST':
        snumber = request.POST['snumber']
        teacher = Person.objects.get(pk=request.POST['teacher'])
        level = request.POST['level']
        position = request.POST['position']
        time = request.POST['time']
        Session.objects.create(session_id=count_index, level_id=level, course_id=get_course_id,
                             position_id=position, time_id=time, session_number=snumber, teacher_id=teacher)
        messages.success(request, 'تم الاضافة بنجاح')
        return HttpResponseRedirect(reverse('add_session'))
    context = {'teacher': teacher,
                }
    return render(request, 'almaher/add_session.html', context)

@login_required(login_url='login')
def edit_session(request, pk):
    # Check request session
    if not request.session.get('get_course_id', False):
        return redirect('select_course')
    get_course_id = request.session['get_course_id']
    get_course_id = Course.objects.get(pk=get_course_id)

    session = Session.objects.get(pk=pk)
    if request.method =='POST':
        get_snumber = request.POST['snumber']
        get_course = request.POST['course']
        get_teacher = request.POST['teacher']
        level = request.POST['level']
        position = request.POST['position']
        time = request.POST['time']
        # 
        course = Course.objects.get(pk=get_course)
        teacher = Person.objects.get(pk=get_teacher)
        # 
        session.session_number = get_snumber
        session.course_id = course
        session.teacher_id = teacher
        session.level_id = level
        session.time_id = time
        session.posistion = position
        session.save()
        messages.success(request, 'Edit success!')
        return HttpResponseRedirect(reverse('session'))
    in_session = Session.objects.all().filter(course_id=get_course_id).filter(~Q(teacher_id=session.teacher_id)).values_list('teacher_id', flat=True)
    teacher = Person.objects.all().filter(type_id__in=('Teacher', 'Graduate')).filter(~Q(pk__in=in_session)).order_by('first_name') #.filter(level_id=session.level_id)
    course = Course.objects.all()
    context = {'session': session,
                'teacher': teacher,
                'course': course,
                }
    return render(request, 'almaher/edit_session.html', context)

@login_required(login_url='login')
def del_session(request, pk):
    get_session = Session.objects.get(pk=pk)
    get_session.delete()
    return redirect('session')

@login_required(login_url='login')
def session_student(request, pk):
    # Check request session
    if not request.session.get('get_course_id', False):
        return redirect('select_course')
    get_course_id = request.session['get_course_id']
    get_course_id = Course.objects.get(pk=get_course_id)

    session = Session.objects.filter(course_id=get_course_id)
    c_session = session.count()

    if request.method =='POST':
        get_snumber = int(request.POST['snumber'])
        session = Session.objects.get(course_id=get_course_id, session_number=get_snumber)
        return redirect('session_student', session.session_id)

    elif c_session != 0:
        global new_pk
        #global to_next 
        #global to_previous
        f_session = session.first()
        l_session = session.last()

        if pk == 1:
            new_pk = f_session.session_id
        else:
            new_pk = pk

        to_next = new_pk
        to_previous = new_pk
        # set to_next & to_previous
        if new_pk == 1:
            to_next = new_pk + 1
        elif new_pk == f_session.session_id:
            to_next = new_pk + 1
        elif new_pk == l_session.session_id:
            to_previous = new_pk - 1
        else:
            to_next = new_pk + 1
            to_previous = new_pk - 1        

        session = Session.objects.get(session_id=new_pk)
        session_student = Session_Student.objects.all().filter(session_id=new_pk)
        list_1 = session_student.values_list('student_id', flat=True)
        # Get student not Enrolment in sessions
        get_session = Session.objects.all().filter(course_id=get_course_id).values_list('session_id', flat=True)
        in_session = Session_Student.objects.all().filter(session_id__in=get_session).values_list('student_id', flat=True)
        # Q objects can be negated with the ~ operator
        student = Person.objects.filter(type_id='Student', level_id=session.level_id, status=True).filter(~Q(pk__in=in_session))
        in_session_teacher = Session.objects.all().filter(pk__in=get_session).filter(~Q(teacher_id=None)).values_list('teacher_id', flat=True)
        teacher = Person.objects.filter(type_id__in=('Teacher', 'Graduate'), level_id=session.level_id, status=True).filter(~Q(pk__in=in_session_teacher)).order_by('first_name')            
        context = {'session': session,
                'session_student': session_student,
                'student': student,
                'f_session': f_session,
                'l_session': l_session,
                'to_next': to_next,
                'to_previous': to_previous,
                'teacher': teacher,
                'c_session': c_session,
                }
        return render(request, 'almaher/session_student.html', context)
    else:
        return redirect('session')


@login_required(login_url='login')
def add_session_student(request, pk, num):
    count_index = Session_Student.objects.all().count()
    if count_index == 0:
        count_index = 1
    else:
        count_index = Session_Student.objects.all().aggregate(Max('id'))['id__max']
        count_index += 1
    session = Session.objects.get(pk=pk)
    student = Person.objects.get(pk=num)
    Session_Student.objects.create(id=count_index, session_id=session, student_id=student)
    return redirect('session_student', pk)

@login_required(login_url='login')
def del_session_student(request, pk, num):
    get_session_student = Session_Student.objects.get(pk=num)
    get_session_student.delete()
    return redirect('session_student', pk)

@login_required(login_url='login')
def view_session_student(request):
    # Check request session
    if not request.session.get('get_course_id', False):
        return redirect('select_course')
    get_course_id = request.session['get_course_id']
    get_course_id = Course.objects.get(pk=get_course_id)

    session = Session.objects.all().filter(course_id=get_course_id).values_list('session_id', flat=True)
    session_student = Session_Student.objects.all().filter(session_id__in=session)
    context = {'session_student': session_student,
                }
    return render(request, 'almaher/view_session_student.html', context)

    
@login_required(login_url='login')
def wait_list_session(request):
    # Check request session
    if not request.session.get('get_course_id', False):
        return redirect('select_course')
    get_course_id = request.session['get_course_id']
    get_course_id = Course.objects.get(pk=get_course_id)

    session = Session.objects.all().filter(course_id=get_course_id)
    get_session = session.values_list('session_id', flat=True)
    in_session = Session_Student.objects.all().filter(session_id__in=get_session).values_list('student_id', flat=True)
    student = Person.objects.filter(type_id='Student', status=True).filter(~Q(pk__in=in_session))
    context = {'student': student,
                'session': session,
                }
    return render(request, 'almaher/wait_list_session.html', context)


# View attendance
@login_required(login_url='login')
def select_attendance(request):
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
    return render(request, 'almaher/attendance_select_course.html', context)

@login_required(login_url='login')
def attendance_generater(request):
    # Check request session
    if not request.session.get('get_course_id', False):
        return redirect('select_course')
    get_course_id = request.session['get_course_id']
    get_course_id = Course.objects.get(pk=get_course_id)
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
    # Check request session
    if not request.session.get('get_course_id', False):
        return redirect('select_course')
    get_course_id = request.session['get_course_id']
    get_course_id = Course.objects.get(pk=get_course_id)
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
    return render(request, 'almaher/attendance_teacher.html', context)

@login_required(login_url='login')
def attendance_student(request):
    # Check request session
    if not request.session.get('get_course_id', False):
        return redirect('select_course')
    get_course_id = request.session['get_course_id']
    get_course_id = Course.objects.get(pk=get_course_id)
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
    return render(request, 'almaher/attendance_student.html', context)    
    
@login_required(login_url='login')
def exam(request):
    # Check request session
    if not request.session.get('get_course_id', False):
        return redirect('select_course')
    get_course_id = request.session['get_course_id']
    get_course_id = Course.objects.get(pk=get_course_id)
    in_session = Session.objects.filter(course_id=get_course_id).values_list('session_id', flat=True)
    get_exam = Exam.objects.filter(session_id__in=in_session)
    student_exam = get_exam.values_list('student_id', flat=True).distinct()
    exam = []
    for all_person in student_exam:
        first_exam = get_exam.filter(student_id=all_person).first()
        all_exam = get_exam.filter(student_id=all_person).values('exam_id', 'type_id', 'time_id', 'mark').order_by('exam_id')
        dic_exam = {'student_id': first_exam.student_id, 'session_id':first_exam.session_id , 'exams': all_exam}
        exam.append(dic_exam)    
    context = {'exam': exam,
                }
    return render(request, 'almaher/exam.html', context)

# Generate exam for all students
@login_required(login_url='login')
def generate_exam(request):
    # Check request session
    if not request.session.get('get_course_id', False):
        return redirect('select_course')
    get_course_id = request.session['get_course_id']
    get_course_id = Course.objects.get(pk=get_course_id)
    # get all students on session in this course and generate 3 type_time and 2 type_exam for each students
    session = Session.objects.all().filter(course_id=get_course_id)
    session_list = session.values_list('session_id', flat=True)
    # Check if student are in exam
    person_in_exam = Exam.objects.filter(session_id__in=session_list).values_list('student_id' ,flat=True)
    session_student = Session_Student.objects.all().filter(session_id__in=session_list)
    student = session_student.filter(~Q(student_id__in=person_in_exam)).values_list('student_id', flat=True)
    # Add student to attendance
    for item in student:
        get_student = Person.objects.get(pk=item)
        get_session_student = session_student.get(student_id=get_student)
        count_index = Exam.objects.all().count()
        if count_index == 0:
            count_index = 1
        else:
            count_index = Exam.objects.all().aggregate(Max('exam_id'))['exam_id__max']
            count_index += 1
        # Add 3 Theoretical
        Exam.objects.create(exam_id=count_index, type_id='نظري', time_id='الامتحان الأول', student_id=get_student, session_id=get_session_student.session_id , mark=0)
        count_index += 1
        Exam.objects.create(exam_id=count_index, type_id='نظري', time_id='التكميلي' , student_id=get_student, session_id=get_session_student.session_id, mark=0)
        count_index += 1
        Exam.objects.create(exam_id=count_index, type_id='نظري', time_id='الاعادة' , student_id=get_student, session_id=get_session_student.session_id, mark=0)
        count_index += 1
        # Add 3 Practical
        Exam.objects.create(exam_id=count_index, type_id='عملي', time_id='الامتحان الأول' , student_id=get_student , session_id=get_session_student.session_id, mark=0)
        count_index += 1
        Exam.objects.create(exam_id=count_index, type_id='عملي', time_id='التكميلي' , student_id=get_student , session_id=get_session_student.session_id, mark=0)
        count_index += 1
        Exam.objects.create(exam_id=count_index, type_id='عملي', time_id='الاعادة' , student_id=get_student , session_id=get_session_student.session_id, mark=0)
        count_index += 1
    messages.success(request, 'تم الانشاء بنجاح')
    return HttpResponseRedirect(reverse('exam'))

# Manage results
@login_required(login_url='login')
def result(request):
    # Check request session
    if not request.session.get('get_course_id', False):
        return redirect('select_course')
    get_course_id = request.session['get_course_id']
    get_course_id = Course.objects.get(pk=get_course_id)
    in_session = Session.objects.filter(course_id=get_course_id).values_list('session_id', flat=True)
    result = Result.objects.filter(session_id__in=in_session)
    context = {'result': result,
                }
    return render(request, 'almaher/result.html', context)

# Generate exam for all students
@login_required(login_url='login')
def generate_result(request):
    # Check request session
    if not request.session.get('get_course_id', False):
        return redirect('select_course')
    get_course_id = request.session['get_course_id']
    get_course_id = Course.objects.get(pk=get_course_id)
    session = Session.objects.all().filter(course_id=get_course_id)
    session_list = session.values_list('session_id', flat=True)
    # Check if student are in result
    result = Result.objects.filter(session_id__in=session_list)
    person_in_result = result.values_list('student_id' ,flat=True)
    session_student = Session_Student.objects.all().filter(session_id__in=session_list)
    student = session_student.filter(~Q(student_id__in=person_in_result)).values_list('student_id', flat=True)
    # Check if any student is not in exam
    session_student_count = session_student.values_list('student_id', flat=True).distinct('student_id')
    chk_exam = Exam.objects.filter(session_id__in=session_list).values_list('student_id', flat=True).distinct('student_id')
    if len(session_student_count) != len(chk_exam):
        messages.error(request, 'الرجاء انشاء الاختبارات ثم انشاء النتائج')
        return HttpResponseRedirect(reverse('result'))
    # Update students on result
    for item in person_in_result:
        get_student = Person.objects.get(pk=item)
        get_result_id = result.get(student_id=get_student)
        get_theoretical_mark = Exam.objects.filter(student_id=get_student, session_id=get_result_id.session_id, type_id='نظري').aggregate(Max('mark'))['mark__max']
        get_practical_mark = Exam.objects.filter(student_id=get_student, session_id=get_result_id.session_id, type_id='عملي').aggregate(Max('mark'))['mark__max']
        get_attendance = Attendance.objects.filter(person_id=get_student, session_id=get_result_id.session_id, status=True).count()
        get_result = (get_theoretical_mark + get_practical_mark) /2
        get_result_type = 'إعادة'
        if get_practical_mark >= 80:
            if get_theoretical_mark >= 80:
                get_result_type = 'ناجح'
            if get_theoretical_mark < 80:
                if get_theoretical_mark >= 70:
                    get_result_type = 'نجاح شرطي'
        # Edit result
        get_result_id.attendance= get_attendance
        get_result_id.theoretical_mark= get_theoretical_mark
        get_result_id.practical_mark= get_practical_mark
        get_result_id.result= get_result
        get_result_id.result_type= get_result_type
        get_result_id.save()
    # Add students to result
    for item in student:
        get_student = Person.objects.get(pk=item)
        get_session_student = session_student.get(student_id=get_student)
        get_theoretical_mark = Exam.objects.filter(student_id=get_student, session_id=get_session_student.session_id, type_id='نظري').aggregate(Max('mark'))['mark__max']
        get_practical_mark = Exam.objects.filter(student_id=get_student, session_id=get_session_student.session_id, type_id='عملي').aggregate(Max('mark'))['mark__max']
        get_attendance = Attendance.objects.filter(person_id=get_student, session_id=get_session_student.session_id, status=True).count()
        get_result = (get_theoretical_mark + get_practical_mark) /2
        get_result_type = 'إعادة'
        if get_practical_mark >= 80:
            if get_theoretical_mark >= 80:
                get_result_type = 'ناجح'
            if get_theoretical_mark < 80:
                if get_theoretical_mark >= 70:
                    get_result_type = 'نجاح شرطي'

        count_index = Result.objects.all().count()
        if count_index == 0:
            count_index = 1
        else:
            count_index = Result.objects.all().aggregate(Max('result_id'))['result_id__max']
            count_index += 1
        # Add result
        Result.objects.create(result_id= count_index,
                                student_id= get_student,
                                session_id= get_session_student.session_id,
                                attendance= get_attendance,
                                theoretical_mark= get_theoretical_mark,
                                practical_mark= get_practical_mark,
                                result= get_result,
                                result_type= get_result_type)
        count_index += 1
    messages.success(request, 'تم الانشاء بنجاح')
    return HttpResponseRedirect(reverse('result'))

@login_required(login_url='login')
def student_pass(request):
    # Check request session
    if not request.session.get('get_course_id', False):
        return redirect('select_course')
    get_course_id = request.session['get_course_id']
    get_course_id = Course.objects.get(pk=get_course_id)
    session = Session.objects.all().filter(course_id=get_course_id)
    session_list = session.values_list('session_id', flat=True)
    # Check if student are in result
    result = Result.objects.filter(session_id__in=session_list)
    person_in_result = result.values_list('student_id' ,flat=True)
    # Check if any student is not in exam
    result_count = result.count()
    if result_count == 0:
        messages.error(request, 'الرجاء انشاء النتائج اولا')
        return HttpResponseRedirect(reverse('result'))
    # Get all students and pass them to next level
    advanced_b = Level.objects.get(pk='متقدم ب')
    advanced_a = Level.objects.get(pk='متقدم أ')
    intermediate_b = Level.objects.get(pk='متوسط ب')
    intermediate_a = Level.objects.get(pk='متوسط أ')
    beginner_b = Level.objects.get(pk='مبتدئ ب')
    beginner_a = Level.objects.get(pk='مبتدئ أ')
    for item in person_in_result:
        get_student = Person.objects.get(pk=item)
        get_result_id = result.get(student_id=get_student)
        this_level = str(get_result_id.session_id.level_id)
        # Check result
        if get_result_id.result_type == 'ناجح':
            if this_level == 'مبتدئ أ':
                get_student.level_id = beginner_b
                get_student.save()
            elif this_level == 'مبتدئ ب':
                get_student.level_id = intermediate_a
                get_student.save()
            elif this_level == 'متوسط أ':
                get_student.level_id = intermediate_b
                get_student.save()
            elif this_level == 'متوسط ب':
                get_student.level_id = advanced_a
                get_student.save()
            elif this_level == 'متقدم أ':
                get_student.level_id = advanced_b
                get_student.save()
            elif this_level == 'متقدم ب':
                get_student.type_id = 'Graduate'
                get_student.status = False
                get_student.save()
            
        elif get_result_id.result_type == 'نجاح شرطي':
            if this_level == 'مبتدئ أ':
                get_student.level_id = beginner_b
                get_student.save()
            elif this_level == 'مبتدئ ب':
                get_student.level_id = intermediate_a
                get_student.save()
            elif this_level == 'متوسط أ':
                get_student.level_id = intermediate_b
                get_student.save()
            elif this_level == 'متوسط ب':
                get_student.level_id = advanced_a
                get_student.save()
            elif this_level == 'متقدم أ':
                get_student.level_id = advanced_b
                get_student.save()
            elif this_level == 'متقدم ب':
                get_student.type_id = 'Graduate'
                get_student.status = False
                get_student.save()

        elif get_result_id.result_type == 'إعادة':
            get_student.level_id = get_result_id.session_id.level_id
            get_student.save()
    messages.success(request, 'تم الترحيل بنجاح')
    return HttpResponseRedirect(reverse('result'))

# Ajax Views
def set_teacher(request):   
    teacher_id = request.GET.get('teacher_id')
    session_id = request.GET.get('session_id')
    get_session = Session.objects.get(pk=session_id)

    if Person.objects.filter(pk=teacher_id).exists():
        get_teacher = Person.objects.get(pk=teacher_id)
        get_session.teacher_id = get_teacher
    else:
        get_session.teacher_id = None
    get_session.save()
    context = {}
    return JsonResponse(context)

def set_student(request):
    # Get index id session student
    count_index_s_student = Session_Student.objects.all().count()
    if count_index_s_student == 0:
        count_index_s_student = 1
    else:
        count_index_s_student = Session_Student.objects.all().aggregate(Max('id'))['id__max']
        count_index_s_student += 1

    student_id = request.GET.get('student_id')
    session_id = request.GET.get('session_id')
    get_session = Session.objects.get(pk=session_id)

    if Person.objects.filter(pk=student_id).exists():
        get_student = Person.objects.get(pk=student_id)
        Session_Student.objects.create(id=count_index_s_student, session_id=get_session, student_id=get_student)
        count_index_s_student += 1
    context = {}
    return JsonResponse(context)

def set_priority(request):   
    student_id = request.GET.get('student_id')
    priority_id = request.GET.get('priority_id')
    if Person.objects.filter(pk=student_id).exists():
        get_student = Person.objects.get(pk=student_id)
        get_student.priority_id = priority_id
        get_student.save()
    context = {}
    return JsonResponse(context)

def set_result_type(request):
    result_id = request.GET.get('result_id')
    result_type = request.GET.get('result_type')
    if Result.objects.filter(pk=result_id).exists():
        get_result = Result.objects.get(pk=result_id)
        get_result.result_type = result_type
        get_result.save()
    print(result_id)
    print(result_type)
    context = {}
    return JsonResponse(context)

def set_exam_mark(request):   
    exam_id = request.GET.get('exam_id')
    exam_value = request.GET.get('exam_value')
    exam = Exam.objects.get(pk=exam_id)
    exam.mark = exam_value
    exam.save()
    context = {}
    return JsonResponse(context)

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

# Test
def get_teacher(request):   
    # Check request session
    if not request.session.get('get_course_id', False):
        return redirect('select_course')
    get_course_id = request.session['get_course_id']
    get_course_id = Course.objects.get(pk=get_course_id)
    teacher_name = ''
    student_id = request.GET.get('student_id')
    student_id = Person.objects.get(pk=student_id)
    get_session = Session.objects.filter(course_id=get_course_id)
    list_session = get_session.values_list('session_id', flat=True)
    # Check person in session
    if Session_Student.objects.get(session_id__in=list_session, student_id=student_id).exists():
        session_student = Session_Student.objects.get(session_id__in=list_session, student_id=student_id)
        session_student = session_student.first()
        t_name = Session.objects.get(session_id=session_student.session_id)
        #teacher_name = str(t_name.teacher_id)
    print(teacher_name)
    data = {'teacher_name': teacher_name}
    return JsonResponse(data)






# Export to *
def export_excel_person(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="persons.xls"'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Persons')
    # Sheet header, first row
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    columns = ['id', 'First name', 'Last name', 'Father name', 'Home number',
                'Phone number', 'Level', 'Birth date', 'Job', 'Address', 'priority', 'status']
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)
    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()
    rows = []
    persons = Person.objects.all().order_by('pk')
    for person in persons:
        id = ''
        fname = ''
        lname = ''
        father_name = ''
        hnumber = ''
        pnumber = ''
        level = ''
        bdate = ''
        job = ''
        address = ''
        priority = ''
        status = ''
        # Check all values if none
        if person.person_id is not None:
            id = person.person_id
        if person.first_name is not None:
            fname = person.first_name
        if person.last_name is not None:
            lname = person.last_name
        if person.father_name is not None:
            father_name = person.father_name
        if person.home_number is not None:
            hnumber = person.home_number
        if person.phone_number is not None:
            pnumber = person.phone_number
        if person.level_id is not None:
            level = str(person.level_id)
        if person.bdate is not None:
            bdate = person.bdate
            bdate = bdate.strftime('%m/%d/%Y')
        if person.job is not None:
            job = person.job
        if person.address is not None:
            address = person.address
        if person.priority_id is not None:
            priority = person.priority_id
        if person.status is not None: 
            status = str(person.status)
        vlues = [id, fname, lname, father_name, hnumber, pnumber,
                 level, bdate, job, address, priority, status]
        rows.append(vlues)
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)
    wb.save(response)
    return response

def export_excel_student(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="students.xls"'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Students')
    # Sheet header, first row
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    columns = ['id', 'First name', 'Last name', 'Father name', 'Home number',
                'Phone number', 'Level', 'Birth date', 'Job', 'Address', 'priority', 'status']
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)
    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()
    rows = []
    persons = Person.objects.all().filter(type_id='Student').order_by('pk')
    for person in persons:
        id = ''
        fname = ''
        lname = ''
        father_name = ''
        hnumber = ''
        pnumber = ''
        level = ''
        bdate = ''
        job = ''
        address = ''
        priority = ''
        status = ''
        # Check all values if none
        if person.person_id is not None:
            id = person.person_id
        if person.first_name is not None:
            fname = person.first_name
        if person.last_name is not None:
            lname = person.last_name
        if person.father_name is not None:
            father_name = person.father_name
        if person.home_number is not None:
            hnumber = person.home_number
        if person.phone_number is not None:
            pnumber = person.phone_number
        if person.level_id is not None:
            level = str(person.level_id)
        if person.bdate is not None:
            bdate = person.bdate
            bdate = bdate.strftime('%m/%d/%Y')
        if person.job is not None:
            job = person.job
        if person.address is not None:
            address = person.address
        if person.priority_id is not None:
            priority = person.priority_id
        if person.status is not None: 
            status = str(person.status)
        vlues = [id, fname, lname, father_name, hnumber, pnumber,
                 level, bdate, job, address, priority, status]
        rows.append(vlues)
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)
    wb.save(response)
    return response

def export_excel_teacher(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="teachers.xls"'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Teachers')
    # Sheet header, first row
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    columns = ['id', 'First name', 'Last name', 'Father name', 'Home number',
                'Phone number', 'Level', 'Birth date', 'Job', 'Address', 'priority', 'status']
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)
    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()
    rows = []
    persons = Person.objects.all().filter(type_id='Teacher').order_by('pk')
    for person in persons:
        id = ''
        fname = ''
        lname = ''
        father_name = ''
        hnumber = ''
        pnumber = ''
        level = ''
        bdate = ''
        job = ''
        address = ''
        priority = ''
        status = ''
        # Check all values if none
        if person.person_id is not None:
            id = person.person_id
        if person.first_name is not None:
            fname = person.first_name
        if person.last_name is not None:
            lname = person.last_name
        if person.father_name is not None:
            father_name = person.father_name
        if person.home_number is not None:
            hnumber = person.home_number
        if person.phone_number is not None:
            pnumber = person.phone_number
        if person.level_id is not None:
            level = str(person.level_id)
        if person.bdate is not None:
            bdate = person.bdate
            bdate = bdate.strftime('%m/%d/%Y')
        if person.job is not None:
            job = person.job
        if person.address is not None:
            address = person.address
        if person.priority_id is not None:
            priority = person.priority_id
        if person.status is not None: 
            status = str(person.status)
        vlues = [id, fname, lname, father_name, hnumber, pnumber,
                 level, bdate, job, address, priority, status]
        rows.append(vlues)
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)
    wb.save(response)
    return response

def export_excel_graduate(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="graduates.xls"'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Graduates')
    # Sheet header, first row
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    columns = ['id', 'First name', 'Last name', 'Father name', 'Home number',
                'Phone number', 'Level', 'Birth date', 'Job', 'Address', 'priority', 'status']
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)
    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()
    rows = []
    persons = Person.objects.all().filter(type_id='Graduate').order_by('pk')
    for person in persons:
        id = ''
        fname = ''
        lname = ''
        father_name = ''
        hnumber = ''
        pnumber = ''
        level = ''
        bdate = ''
        job = ''
        address = ''
        priority = ''
        status = ''
        # Check all values if none
        if person.person_id is not None:
            id = person.person_id
        if person.first_name is not None:
            fname = person.first_name
        if person.last_name is not None:
            lname = person.last_name
        if person.father_name is not None:
            father_name = person.father_name
        if person.home_number is not None:
            hnumber = person.home_number
        if person.phone_number is not None:
            pnumber = person.phone_number
        if person.level_id is not None:
            level = str(person.level_id)
        if person.bdate is not None:
            bdate = person.bdate
            bdate = bdate.strftime('%m/%d/%Y')
        if person.job is not None:
            job = person.job
        if person.address is not None:
            address = person.address
        if person.priority_id is not None:
            priority = person.priority_id
        if person.status is not None: 
            status = str(person.status)
        vlues = [id, fname, lname, father_name, hnumber, pnumber,
                 level, bdate, job, address, priority, status]
        rows.append(vlues)
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)
    wb.save(response)
    return response

def export_excel_attendance(request):    
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="attendance_teacher.xls"'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Students')
    # Sheet header, first row
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    teacher = Person.objects.all().filter(type_id='Teacher').values_list('person_id', flat=True)
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

def export_session_pdf(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="session.pdf"'
    response['Content-Transform-Encoding'] = 'binary'
    if not request.session.get('get_course_id', False):
        return redirect('select_course')
    get_course_id = request.session['get_course_id']
    get_course_id = Course.objects.get(pk=get_course_id)
    num_of_session = get_course_id.num_of_session
    num_of_session_list = []
    for i in range(num_of_session):
        num_of_session_list.append(i)
    num_of_session += 2
    num_of_session_list2 = []
    for i in range(num_of_session):
        num_of_session_list2.append(i)
    session = Session.objects.filter(course_id=get_course_id).order_by('session_id')
    session_list = session.values_list('session_id', flat=True)
    student = Session_Student.objects.filter(session_id__in=session_list)
    # Check if any student is not in attendance
    chk_attendance = Attendance.objects.filter(session_id__in=session_list).distinct('person_id').count()
    if chk_attendance == 0:
        messages.error(request, 'الرجاء انشاء الحضور اولا')
        return HttpResponseRedirect(reverse('session'))
    c_session = session.count()
    day = Attendance.objects.filter(session_id__in=session_list).order_by('day').distinct('day').values_list('day', flat=True)
    context = {'session': session,
                'student': student,
                'num_of_session': num_of_session,
                'num_of_session_list': num_of_session_list,
                'num_of_session_list2': num_of_session_list2,
                'course_name': get_course_id.course_name,
                'day': day,
                }
    html_string = render_to_string('almaher/pdf_output.html', context)
    html = HTML(string=html_string)
    result = html.write_pdf()
    with tempfile.NamedTemporaryFile(delete=True) as output:
        output.write(result)
        output.flush()
        output = open(output.name, 'rb')
        response.write(output.read())
    return response

def export_students_session_pdf(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="students_session.pdf"'
    response['Content-Transform-Encoding'] = 'binary'
    if not request.session.get('get_course_id', False):
        return redirect('select_course')
    get_course_id = request.session['get_course_id']
    get_course_id = Course.objects.get(pk=get_course_id)
    session = Session.objects.filter(course_id=get_course_id).order_by('session_id')
    session_list = session.values_list('session_id', flat=True)
    student = Session_Student.objects.filter(session_id__in=session_list)
    c_session_std = int(student.count())
    c_session_std += 1
    count = []
    for i in range(1, c_session_std):
        count.append(i)
    student = zip(student, count)
    context = {'student': student,
                'course_name': get_course_id.course_name,
                }
    html_string = render_to_string('almaher/pdf_session_student.html', context)
    html = HTML(string=html_string)
    result = html.write_pdf()
    with tempfile.NamedTemporaryFile(delete=True) as output:
        output.write(result)
        output.flush()
        output = open(output.name, 'rb')
        response.write(output.read())
    return response

def export_teacher_session_pdf(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="teachers_session.pdf"'
    response['Content-Transform-Encoding'] = 'binary'
    if not request.session.get('get_course_id', False):
        return redirect('select_course')
    get_course_id = request.session['get_course_id']
    get_course_id = Course.objects.get(pk=get_course_id)
    session = Session.objects.filter(course_id=get_course_id).order_by('session_id')
    c_session = int(session.count())
    c_session += 1
    count = []
    for i in range(1, c_session):
        count.append(i)
    session = zip(session, count)
    context = {'session': session,
                'course_name': get_course_id.course_name,
                }
    html_string = render_to_string('almaher/pdf_session_teacher.html', context)
    html = HTML(string=html_string)
    result = html.write_pdf()
    with tempfile.NamedTemporaryFile(delete=True) as output:
        output.write(result)
        output.flush()
        output = open(output.name, 'rb')
        response.write(output.read())
    return response