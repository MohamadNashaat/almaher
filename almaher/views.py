from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
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
        return HttpResponseRedirect(reverse('add_teacher'))
    
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
    


def student(request):
    student = Person.objects.all().filter(type_id=2)
    c_student = student.count()
    context = {'c_student': c_student,
                'student': student}
    return render(request, 'almaher/student.html', context)


def add_student(request):
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
            level = Level.objects.get(pk=level_id)
            new_teacher = Person(type_id=p_type, first_name=fname, last_name=lname,
                            father_name=father_n, home_number=hn, phone_number=pn,
                            job=j, address=ad, bdate=bd, level_id=level)
        else:
            new_teacher = Person(type_id=p_type, first_name=fname, last_name=lname,
                            father_name=father_n, home_number=hn, phone_number=pn,
                            job=j, address=ad, bdate=bd)              
        new_teacher.save()
        messages.success(request, 'Add success!')
        return HttpResponseRedirect(reverse('add_student'))
    return render(request, 'almaher/add_student.html')


def edit_student(request, pk):
    student = Person.objects.get(person_id=pk)
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
    return render(request, 'almaher/edit_student.html', {'student': student})

def del_student(request, pk):
    student = Person.objects.get(person_id=pk)
    if request.method =='POST':
        student.delete()
        return redirect('student')
    return render(request, 'almaher/del_student.html', {'student': student})

def session(request):
    return render(request, 'almaher/session.html')

