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
    context = {'c_teacher': c_teacher, 
                'c_student': c_student,
                'c_graduate': c_graduate,
                'c_course': c_course,
                'c_session': c_session,
                'get_course_id': get_course_id,
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
        messages.success(request, 'Add success!')
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
        level = Level.objects.get(pk=level)
        Person.objects.create(person_id=count_index, type_id='Student', first_name=fname, last_name=lname,
                        father_name=father_n, home_number=hn, phone_number=pn,
                        job=j, address=ad, bdate=bd, level_id=level)
        messages.success(request, 'Add success!')
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
    course = Course.objects.all()
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
        Course.objects.create(course_id=count_index, course_name=ncourse, start_date=sdate, end_date=edate)
        messages.success(request, 'Add success!')
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
    c_session = session.count()
    session_list = []
    if c_session != 0:
        for s_loop in range(1,136):
            get_session = session.get(session_number=s_loop)
            c_student = Session_Student.objects.filter(session_id=get_session).count()
            session_list.append(c_student)
    zip_list = zip(session, session_list)
    context = {'zip_list': zip_list,
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
    person_list = []
    level_list = Level.objects.all().values_list('level_name', flat=True)
    for level_loop in level_list:
        l_count = Person.objects.filter(level_id=level_loop).count()
        person_list.append(l_count)
    zip_list = zip(level_list, person_list)

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
            # Positions
            p1 = Position.objects.get(pk='توسعة مكتبة')
            p2 = Position.objects.get(pk='قبو')
            p3 = Position.objects.get(pk='توسعة حرم رئيسي')
            p4 = Position.objects.get(pk='حرم رئيسي')
            p5 = Position.objects.get(pk='تحت السدة')
            # Loop to create sessons
            for l1 in range(1,16):
                new_session = Session(session_id=count_index, level_id=advanced_b,course_id=get_course_id,session_number=l1, time_id=time, position_id=p1)
                new_session.save()
                count_index += 1

                get_session = Session.objects.all().filter(course_id=get_course_id).values_list('session_id', flat=True)
                in_session = Session_Student.objects.all().filter(session_id__in=get_session).values_list('student_id', flat=True)
                student = Person.objects.filter(~Q(pk__in=in_session)).filter(type_id='Student', status=True, level_id=new_session.level_id).order_by('bdate').values_list('person_id', flat=True)
                
                var_num = 0
                for s_loop in range(1,7): # add six stuents to every session
                    if var_num < len(student):
                        get_student = int(student[var_num])
                        new_student = Person.objects.get(pk=get_student)
                        Session_Student.objects.create(id=count_index_s_student, session_id=new_session, student_id=new_student)
                        var_num += 1
                        count_index_s_student += 1
                    else:
                        break

            for l1 in range(16,41):
                new_session = Session(session_id=count_index, level_id=advanced_a,course_id=get_course_id,session_number=l1, time_id=time, position_id=p2)
                new_session.save()
                count_index += 1

                get_session = Session.objects.all().filter(course_id=get_course_id).values_list('session_id', flat=True)
                in_session = Session_Student.objects.all().filter(session_id__in=get_session).values_list('student_id', flat=True)
                student = Person.objects.filter(~Q(pk__in=in_session)).filter(type_id='Student', status=True, level_id=new_session.level_id).order_by('bdate').values_list('person_id', flat=True) 
                
                var_num = 0
                for s_loop in range(1,7): # add six stuents to every session
                    if var_num < len(student):
                        get_student = int(student[var_num])
                        new_student = Person.objects.get(pk=get_student)
                        Session_Student.objects.create(id=count_index_s_student, session_id=new_session, student_id=new_student)
                        var_num += 1
                        count_index_s_student += 1
                    else:
                        break

            for l1 in range(41,66):
                new_session = Session(session_id=count_index, level_id=intermediate_b,course_id=get_course_id,session_number=l1, time_id=time, position_id=p3)
                new_session.save()
                count_index += 1

                get_session = Session.objects.all().filter(course_id=get_course_id).values_list('session_id', flat=True)
                in_session = Session_Student.objects.all().filter(session_id__in=get_session).values_list('student_id', flat=True)
                student = Person.objects.filter(~Q(pk__in=in_session)).filter(type_id='Student', status=True, level_id=new_session.level_id).order_by('bdate').values_list('person_id', flat=True) 
                
                var_num = 0
                for s_loop in range(1,7): # add six stuents to every session
                    if var_num < len(student):
                        get_student = int(student[var_num])
                        new_student = Person.objects.get(pk=get_student)
                        Session_Student.objects.create(id=count_index_s_student, session_id=new_session, student_id=new_student)
                        var_num += 1
                        count_index_s_student += 1
                    else:
                        break

            for l1 in range(66,91):
                new_session = Session(session_id=count_index, level_id=intermediate_a,course_id=get_course_id,session_number=l1, time_id=time, position_id=p4)
                new_session.save()
                count_index += 1

                get_session = Session.objects.all().filter(course_id=get_course_id).values_list('session_id', flat=True)
                in_session = Session_Student.objects.all().filter(session_id__in=get_session).values_list('student_id', flat=True)
                student = Person.objects.filter(~Q(pk__in=in_session)).filter(type_id='Student', status=True, level_id=new_session.level_id).order_by('bdate').values_list('person_id', flat=True) 
                
                var_num = 0
                for s_loop in range(1,7): # add six stuents to every session
                    if var_num < len(student):
                        get_student = int(student[var_num])
                        new_student = Person.objects.get(pk=get_student)
                        Session_Student.objects.create(id=count_index_s_student, session_id=new_session, student_id=new_student)
                        var_num += 1
                        count_index_s_student += 1
                    else:
                        break

            for l1 in range(91,116):
                new_session = Session(session_id=count_index, level_id=beginner_b,course_id=get_course_id,session_number=l1, time_id=time, position_id=p5)
                new_session.save()
                count_index += 1

                get_session = Session.objects.all().filter(course_id=get_course_id).values_list('session_id', flat=True)
                in_session = Session_Student.objects.all().filter(session_id__in=get_session).values_list('student_id', flat=True)
                student = Person.objects.filter(~Q(pk__in=in_session)).filter(type_id='Student', status=True, level_id=new_session.level_id).order_by('bdate').values_list('person_id', flat=True) 
                
                var_num = 0
                for s_loop in range(1,7): # add six stuents to every session
                    if var_num < len(student):
                        get_student = int(student[var_num])
                        new_student = Person.objects.get(pk=get_student)
                        Session_Student.objects.create(id=count_index_s_student, session_id=new_session, student_id=new_student)
                        var_num += 1
                        count_index_s_student += 1
                    else:
                        break

            for l1 in range(116,136):
                new_session = Session(session_id=count_index, level_id=beginner_a,course_id=get_course_id,session_number=l1, time_id=time, position_id=p1)
                new_session.save()
                count_index += 1

                get_session = Session.objects.all().filter(course_id=get_course_id).values_list('session_id', flat=True)
                in_session = Session_Student.objects.all().filter(session_id__in=get_session).values_list('student_id', flat=True)
                student = Person.objects.filter(~Q(pk__in=in_session)).filter(type_id='Student', status=True, level_id=new_session.level_id).order_by('bdate').values_list('person_id', flat=True) 
                
                var_num = 0
                for s_loop in range(1,7): # add six stuents to every session
                    if var_num < len(student):
                        get_student = int(student[var_num])
                        new_student = Person.objects.get(pk=get_student)
                        Session_Student.objects.create(id=count_index_s_student, session_id=new_session, student_id=new_student)
                        var_num += 1
                        count_index_s_student += 1
                    else:
                        break

            # Loop to add students to sessions
            #student = Person.objects.filter(type_id='Student', status=True).order_by('bdate').values_list('person_id', flat=True)  # level_id=session.level_id
            # 
            #var_num = 0
            #for session_loop in range(1,136):
            #    session = Session.objects.get(course_id=get_course_id, session_number=session_loop)
            #    for student_loop in range(1,5): # add four stuents to every session
            #        get_student = int(student[var_num])
            #        new_student = Person.objects.get(pk=get_student)
            #        Session_Student.objects.create(session_id=session, student_id=new_student)
            #        var_num += 1

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
        messages.success(request, 'Add success!')
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

    c_session_stud = Session.objects.count()

    if request.method =='POST':
            get_snumber = int(request.POST['snumber'])
            session = Session.objects.get(course_id=get_course_id, session_number=get_snumber)
            return redirect('session_student', session.session_id)

    elif c_session_stud != 0:
        global new_pk
        #global to_next 
        #global to_previous
        f_session = Session.objects.first()
        l_session = Session.objects.last()

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
        # Get student not Enrolment in sessions
        get_session = Session.objects.all().filter(course_id=get_course_id).values_list('session_id', flat=True)
        in_session = Session_Student.objects.all().filter(session_id__in=get_session).values_list('student_id', flat=True)
        # Q objects can be negated with the ~ operator
        student = Person.objects.filter(type_id='Student', level_id=session.level_id, status=True).filter(~Q(pk__in=in_session))
        in_session_teacher = Session.objects.all().filter(session_id__in=get_session).values_list('teacher_id', flat=True)
        teacher = Person.objects.filter(type_id__in=('Teacher', 'Graduate'), level_id=session.level_id, status=True).order_by('first_name')#.filter(~Q(pk__in=in_session_teacher))#.order_by('first_name')
        context = {'session': session,
                'session_student': session_student,
                'student': student,
                'f_session': f_session,
                'l_session': l_session,
                'to_next': to_next,
                'to_previous': to_previous,
                'teacher': teacher,
                }
        return render(request, 'almaher/session_student.html', context)
    else:
        return redirect('session')
    
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

    course = Course.objects.all()
    if request.method =='POST':
        get_sdate = get_course_id.start_date
        get_num = int(request.POST['num'])
        new_date = []
        for i in range(get_num):
            new_date.append(get_sdate)
            get_sdate = get_sdate + timedelta(days=7)
        # Get course id
        session = Session.objects.all().filter(course_id=get_course_id)
        session_list = session.values_list('session_id', flat=True)
        # Check if teacher or student are in attendance
        person_in_attandance = Attendance.objects.filter(session_id__in=session_list).values_list('person_id' ,flat=True)
        ###
        person_list = Person.objects.all().values_list('person_id' ,flat=True)
        teacher = session.filter(teacher_id__in=person_list).filter(~Q(teacher_id__in=person_in_attandance)).values_list('teacher_id', flat=True)
        session_student = Session_Student.objects.all().filter(session_id__in=session_list)
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
        
        messages.success(request, 'Add success!')
        return HttpResponseRedirect(reverse('attendance'))
    context = {'course': course,
                
                }
    return render(request, 'almaher/attendance_generater.html', context)

@login_required(login_url='login')
def attendance_teacher(request):
    # Check request session
    if not request.session.get('get_course_id', False):
        return redirect('select_course')
    get_course_id = request.session['get_course_id']
    get_course_id = Course.objects.get(pk=get_course_id)

    teacher = Person.objects.all().filter(type_id='Teacher').values_list('person_id', flat=True)
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
    # Check request session
    if not request.session.get('get_course_id', False):
        return redirect('select_course')
    get_course_id = request.session['get_course_id']
    get_course_id = Course.objects.get(pk=get_course_id)

    student = Person.objects.all().filter(type_id='Student').values_list('person_id', flat=True)
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
    context = {}
    return JsonResponse(context)

def change_status_false(request):   
    attendance_id = request.GET.get('attendance_id')
    attendance = Attendance.objects.get(pk=attendance_id)
    attendance.status = False
    attendance.save()
    context = {}
    return JsonResponse(context)


# Views exam
@login_required(login_url='login')
def select_exam(request):
    # Check request session
    if not request.session.get('get_course_id', False):
        return redirect('select_course')
    get_course_id = request.session['get_course_id']
    get_course_id = Course.objects.get(pk=get_course_id)

    course = Course.objects.all()
    if request.method =='POST':
        get_type = request.POST['type']
        get_time = request.POST['time']
        request.session['exam_type'] = get_type
        request.session['exam_time'] = get_time
        return redirect('exam')
    context = {'course': course,
                }
    return render(request, 'almaher/exam_select.html', context)        
    

@login_required(login_url='login')
def exam(request):
    # Check request session
    if not request.session.get('get_course_id', False):
        return redirect('select_course')
    get_course_id = request.session['get_course_id']
    get_course_id = Course.objects.get(pk=get_course_id)

    #get_type = request.session['exam_type']
    #get_time = request.session['exam_time']
    
    in_session = Session.objects.filter(course_id=get_course_id).values_list('session_id', flat=True)
    exam = Exam.objects.filter(session_id__in=in_session) #, time_id=get_time, type_id=get_type)
    context = {'exam': exam,
                }
    return render(request, 'almaher/exam.html', context)


@login_required(login_url='login')
def add_theoretical_exam(request):
    # Check request session
    if not request.session.get('get_course_id', False):
        return redirect('select_course')
    get_course_id = request.session['get_course_id']
    get_course_id = Course.objects.get(pk=get_course_id)

    get_session = Session.objects.all().filter(course_id=get_course_id).values_list('session_id', flat=True)
    in_session = Session_Student.objects.all().filter(session_id__in=get_session).values_list('student_id', flat=True)
    student = Person.objects.filter(pk__in=in_session, type_id='Student', status=True)
    teacher = Person.objects.all().filter(type_id__in=('Teacher', 'Graduate'), status=True)   
    
    if request.method == 'POST':
        count_index = Exam.objects.all().count()
        if count_index == 0:
            count_index = 1
        else:
            count_index = Exam.objects.all().aggregate(Max('exam_id'))['exam_id__max']
            count_index += 1
        get_time = request.POST['time']
        mark = request.POST['mark']
        student = request.POST['student']
        student = Person.objects.get(pk=student)

        in_session = Session.objects.filter(course_id=get_course_id).values_list('session_id', flat=True)
        session = Session_Student.objects.get(session_id__in=in_session, student_id=student)

        Exam.objects.create(exam_id=count_index, type_id='نظري', time_id=get_time, 
        student_id=student, session_id=session.session_id, mark=mark)
        
        messages.success(request, 'Add success!')
        return HttpResponseRedirect(reverse('add_theoretical_exam')) 
    context = {'student': student,
                'teacher': teacher,
                }
    return render(request, 'almaher/add_theoretical_exam.html', context)

@login_required(login_url='login')
def add_practical_exam(request):
    # Check request session
    if not request.session.get('get_course_id', False):
        return redirect('select_course')
    get_course_id = request.session['get_course_id']
    get_course_id = Course.objects.get(pk=get_course_id)

    get_session = Session.objects.all().filter(course_id=get_course_id).values_list('session_id', flat=True)
    in_session = Session_Student.objects.all().filter(session_id__in=get_session).values_list('student_id', flat=True)
    student = Person.objects.filter(pk__in=in_session, type_id='Student', status=True)
    teacher = Person.objects.all().filter(type_id__in=('Teacher', 'Graduate'), status=True)   
    
    if request.method == 'POST':
        count_index = Exam.objects.all().count()
        if count_index == 0:
            count_index = 1
        else:
            count_index = Exam.objects.all().aggregate(Max('exam_id'))['exam_id__max']
            count_index += 1
        get_time = request.POST['time']
        mark = request.POST['mark']
        student = request.POST['student']
        student = Person.objects.get(pk=student)
        teacher = request.POST['teacher']
        teacher = Person.objects.get(pk=teacher)

        in_session = Session.objects.filter(course_id=get_course_id).values_list('session_id', flat=True)
        session = Session_Student.objects.get(session_id__in=in_session, student_id=student)

        Exam.objects.create(exam_id=count_index, type_id='عملي', time_id=get_time, 
        student_id=student, teacher_id=teacher, session_id=session.session_id, mark=mark)
        
        messages.success(request, 'Add success!')
        return HttpResponseRedirect(reverse('add_practical_exam'))
    context = {'student': student,
                'teacher': teacher,
                }
    return render(request, 'almaher/add_practical_exam.html', context)


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

    persons = Person.objects.all().filter(type_id='Student')
    
    for person in persons:
        person_bd = person.bdate
        person_bd = person_bd.strftime('%m/%d/%Y')
        vlues = [person.person_id, person.first_name, person.last_name, person.father_name, 
            person.home_number, person.phone_number, person.level_id, person_bd,
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

    persons = Person.objects.all().filter(type_id='Teacher')
    
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

    student = Person.objects.all().filter(type_id='Student').values_list('person_id', flat=True)
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
