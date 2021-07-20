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

from course.tests import get_request_session_course_id

# Create your views here.

@login_required(login_url='login')
def result(request):
    get_course_id = get_request_session_course_id(request)
    in_session = Session.objects.filter(course_id=get_course_id).values_list('session_id', flat=True)
    result = Result.objects.filter(session_id__in=in_session)
    context = {'result': result,
                'get_course_id': get_course_id,
                }
    return render(request, 'result/result.html', context)

# Generate exam for all students
@login_required(login_url='login')
def generate_result(request):
    get_course_id = get_request_session_course_id(request)
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
    if request.user.is_staff:
        get_course_id = get_request_session_course_id(request)
        session = Session.objects.all().filter(course_id=get_course_id)
        session_list = session.values_list('session_id', flat=True)
        # Check if student are in result
        result = Result.objects.filter(session_id__in=session_list)
        exam = Exam.objects.filter(session_id__in=session_list)
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
                get_student.priority_id = 'مستمر'
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
                    get_student.level_id = beginner_a
                    get_student.save()
            elif get_result_id.result_type == 'نجاح شرطي':
                get_student.priority_id = 'مستمر'
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
                    get_student.level_id = beginner_a
                    get_student.save()
            elif get_result_id.result_type == 'إعادة':
                get_student = Person.objects.get(pk=item)
                get_theoretical_mark = exam.filter(student_id=get_student, type_id='نظري').aggregate(Max('mark'))['mark__max']
                get_practical_mark = exam.filter(student_id=get_student, type_id='عملي').aggregate(Max('mark'))['mark__max']
                if get_practical_mark == 0 and get_theoretical_mark == 0:
                    get_student.level_id = get_result_id.session_id.level_id
                    get_student.priority_id = 'غير معروف'
                    get_student.save()
                else:
                    get_student.priority_id = 'مستمر'
                    get_student.level_id = get_result_id.session_id.level_id
                    get_student.save()
        messages.success(request, 'تم الترحيل بنجاح')
        return HttpResponseRedirect(reverse('result'))
    messages.warning(request, 'ليس لديك صلاحية للقيام بهذه العملية')
    return redirect('result')

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