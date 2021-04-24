from django.db import models

class Person(models.Model):
    level = (
        ('مبتدئ أ' ,'مبتدئ أ'),
        ('مبتدئ ب' ,'مبتدئ ب'),
        ('متوسط أ' ,'متوسط أ'),
        ('متوسط ب' ,'متوسط ب'),
        ('متقدم أ', 'متقدم أ'),
        ('متقدم ب', 'متقدم ب'),
    )
    person_type = (
        ('Teacher', 'Teacher'),
        ('Student', 'Student'),
        ('Graduate', 'Graduate'),
    )
    person_id = models.AutoField(primary_key=True)
    type_id = models.CharField(max_length=50, null=True, choices=person_type)
    first_name = models.CharField(max_length=120, null=True)
    last_name = models.CharField(max_length=120, null=True)
    father_name = models.CharField(max_length=120, null=True)
    home_number = models.CharField(max_length=120, null=True)
    phone_number = models.CharField(max_length=120, null=True)
    job = models.CharField(max_length=120, null=True)
    address = models.CharField(max_length=120, null=True)
    bdate = models.DateField(null=True)
    level_id = models.CharField(max_length=50, null=True, choices=level)
    status = models.BooleanField(default=True, null=True)
    create_date = models.DateField(auto_now_add=True, null=True)
    def __str__(self):
        return f'{self.first_name} {self.last_name}'

class Course(models.Model):
    course_id = models.AutoField(primary_key=True)
    course_name = models.CharField(max_length=120)
    start_date = models.DateField(null=True)
    end_date = models.DateField(null=True)
    def __str__(self):
        return self.course_name

class Session(models.Model):
    level = (
        ('مبتدئ أ' ,'مبتدئ أ'),
        ('مبتدئ ب' ,'مبتدئ ب'),
        ('متوسط أ' ,'متوسط أ'),
        ('متوسط ب' ,'متوسط ب'),
        ('متقدم أ', 'متقدم أ'),
        ('متقدم ب', 'متقدم ب'),
    )
    time = (
        ('بعد جلسة الصفا' ,'بعد جلسة الصفا'),
    )
    position = (
        ('حرم رئيسي' ,'حرم رئيسي'),
        ('توسعة حرم رئيسي' ,'توسعة حرم رئيسي'),
        ('تحت السدة' ,'تحت السدة'),
        ('توسعة مكتبة' ,'توسعة مكتبة'),
        ('قبو' ,'قبو'),
    )
    session_id = models.AutoField(primary_key=True)
    session_number = models.IntegerField()
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE)
    level_id = models.CharField(max_length=50, null=True, choices=level)
    position_id = models.CharField(max_length=50, null=True, choices=position)
    time_id = models.CharField(max_length=50, null=True, choices=time)
    teacher_id = models.ForeignKey(Person, null=True, on_delete=models.SET_NULL)
    def __str__(self):
        return f'{self.session_id}'

class Session_Student(models.Model):
    id = models.AutoField(primary_key=True)
    session_id = models.ForeignKey(Session, on_delete=models.CASCADE)
    student_id = models.ForeignKey(Person, on_delete=models.CASCADE)
    def __str__(self):
        return f'{self.id}'

class Attendance(models.Model):
    attendance_id = models.AutoField(primary_key=True)
    person_id = models.ForeignKey(Person, on_delete=models.CASCADE)
    session_id = models.ForeignKey(Session, on_delete=models.CASCADE)
    day = models.DateField()
    status = models.BooleanField()
    def __str__(self):
        return f'{self.day}'

#class Exam_Type(models.Model):
#    exam_type_id = models.AutoField(primary_key=True)
#    exam_type_name = models.CharField(max_length=120)
#    def __str__(self):
#        return f'{self.exam_type_name}'
#    #exam_type_id = 1 ==> نظري
#    #exam_type_id = 2 ==> عملي

#class Exam_Time(models.Model):
#    exam_time_id = models.AutoField(primary_key=True)
#    exam_time_name = models.CharField(max_length=120)
#    def __str__(self):
#        return f'{self.exam_time_name}'
#    #exam_time_id = 1 ==> الامتحان الأول
#    #exam_time_id = 2 ==> التكميلي
#    #exam_time_id = 3 ==> الاعادة 

#class Exam(models.Model):
#    exam_id = models.AutoField(primary_key=True)
#    exam_type_id = models.ForeignKey(Exam_Type, on_delete=models.CASCADE)
#    exam_time_id = models.ForeignKey(Exam_Time, on_delete=models.CASCADE)
#    student_id = models.ForeignKey(Person, on_delete=models.CASCADE)
#    teacher_id = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='teacher_id')
#    session_id = models.ForeignKey(Session, on_delete=models.CASCADE)
#    first_mark = models.FloatField(null=True)
#    second_mark = models.FloatField(null=True)
#    result = models.FloatField()