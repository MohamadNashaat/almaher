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
    return render(request, 'session/session.html', context)

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
        l_count = Person.objects.filter(type_id='Student' ,level_id=level_loop, status=True).count()
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
                new_session = Session(session_id=count_index, level_id=intermediate_b,course_id=get_course_id,session_number=l1, time_id=time, position_id=p4)
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
                new_session = Session(session_id=count_index, level_id=intermediate_a,course_id=get_course_id,session_number=l1, time_id=time, position_id=p3)
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
    return render(request, 'session/generate_session.html', context)

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
    return render(request, 'session/add_session.html', context)

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
    return render(request, 'session/edit_session.html', context)

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
        return render(request, 'session/session_student.html', context)
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
    return render(request, 'session/view_session_student.html', context)

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
    return render(request, 'session/wait_list_session.html', context)

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
    html_string = render_to_string('session/pdf_output.html', context)
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
    html_string = render_to_string('session/pdf_session_student.html', context)
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
    html_string = render_to_string('session/pdf_session_teacher.html', context)
    html = HTML(string=html_string)
    result = html.write_pdf()
    with tempfile.NamedTemporaryFile(delete=True) as output:
        output.write(result)
        output.flush()
        output = open(output.name, 'rb')
        response.write(output.read())
    return response

def export_students_session_excel(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="session_students.xls"'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Persons')
    # Sheet header, first row
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    columns = ['id', 'First name', 'Last name', 'Home number',
                'Phone number', 'Session', 'Level', 'Position']
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)
    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()
    rows = []
    get_course_id = request.session['get_course_id']
    get_course_id = Course.objects.get(pk=get_course_id)
    session = Session.objects.filter(course_id=get_course_id).order_by('session_id')
    session_list = session.values_list('session_id', flat=True)
    student = Session_Student.objects.filter(session_id__in=session_list)
    for s in student:
        id = ''
        fname = ''
        lname = ''
        hnumber = ''
        pnumber = ''
        level = ''
        session = ''
        position = ''
        # Check all values if none
        if s.student_id.person_id is not None:
            id = s.student_id.person_id
        if s.student_id.first_name is not None:
            fname = s.student_id.first_name
        if s.student_id.last_name is not None:
            lname = s.student_id.last_name
        if s.student_id.home_number is not None:
            hnumber = s.student_id.home_number
        if s.student_id.phone_number is not None:
            pnumber = s.student_id.phone_number
        if s.session_id.level_id is not None:
            level = str(s.session_id.level_id)
        if s.session_id.session_number is not None:
            session = s.session_id.session_number
        if s.session_id.position_id is not None:
            position = str(s.session_id.position_id)
        vlues = [id, fname, lname, hnumber, pnumber,
                 level, session, position]
        rows.append(vlues)
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)
    wb.save(response)
    return response

def export_teachers_session_excel(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="session_teachers.xls"'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Persons')
    # Sheet header, first row
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    columns = ['id', 'First name', 'Last name', 'Home number',
                'Phone number', 'Session', 'Level', 'Position']
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)
    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()
    rows = []
    get_course_id = request.session['get_course_id']
    get_course_id = Course.objects.get(pk=get_course_id)
    teacher = Session.objects.filter(course_id=get_course_id).order_by('session_id')
    teacher = teacher.filter(~Q(teacher_id=None))
    for t in teacher:
        id = ''
        fname = ''
        lname = ''
        hnumber = ''
        pnumber = ''
        level = ''
        session = ''
        position = ''
        # Check all values if none
        if t.teacher_id.person_id is not None:
            id = t.teacher_id.person_id
        if t.teacher_id.first_name is not None:
            fname = t.teacher_id.first_name
        if t.teacher_id.last_name is not None:
            lname = t.teacher_id.last_name
        if t.teacher_id.home_number is not None:
            hnumber = t.teacher_id.home_number
        if t.teacher_id.phone_number is not None:
            pnumber = t.teacher_id.phone_number
        if t.level_id is not None:
            level = str(t.level_id)
        if t.session_number is not None:
            session = t.session_number
        if t.position_id is not None:
            position = str(t.position_id)
        vlues = [id, fname, lname, hnumber, pnumber,
                 level, session, position]
        rows.append(vlues)
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)
    wb.save(response)
    return response