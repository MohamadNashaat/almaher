from django.shortcuts import render
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
    context = {'c_teacher': c_teacher, 
                'c_student': c_student}
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
    return render(request, 'almaher/edit_teacher.html', {'teacher': teacher})


def student(request):
    student = Person.objects.all().filter(type_id=2)
    c_student = student.count()
    context = {'c_student': c_student,
                'student': student}
    return render(request, 'almaher/student.html', context)


def add_student(request):
    return render(request, 'almaher/add_student.html')


def edit_student(request, pk):
    student = Person.objects.get(person_id=pk)
    return render(request, 'almaher/edit_student.html', {'student': student})

def del_student(request, pk):
    pass