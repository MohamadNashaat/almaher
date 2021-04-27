from django.db import models

class Person(models.Model):
    level = (
        ('مبتدئ أ','مبتدئ أ'),
        ('مبتدئ ب','مبتدئ ب'),
        ('متوسط أ','متوسط أ'),
        ('متوسط ب','متوسط ب'),
        ('متقدم أ','متقدم أ'),
        ('متقدم ب','متقدم ب'),
    )
    person_type = (
        ('Teacher','Teacher'),
        ('Student','Student'),
        ('Graduate','Graduate'),
    )
    priority = (
        ('مستمر','مستمر'),
        ('غير معروف','غير معروف'),
    )
    person_id = models.IntegerField(primary_key=True)
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
    priority_id = models.CharField(max_length=50, null=True, choices=priority)
    status = models.BooleanField(default=True, null=True)
    create_date = models.DateField(auto_now_add=True, null=True)
    def __str__(self):
        return f'{self.first_name} {self.last_name}'

class Course(models.Model):
    course_id = models.IntegerField(primary_key=True)
    course_name = models.CharField(max_length=120)
    start_date = models.DateField(null=True)
    end_date = models.DateField(null=True)
    create_date = models.DateField(auto_now_add=True, null=True)
    def __str__(self):
        return self.course_name

class Session(models.Model):
    level = (
        ('مبتدئ أ','مبتدئ أ'),
        ('مبتدئ ب','مبتدئ ب'),
        ('متوسط أ','متوسط أ'),
        ('متوسط ب','متوسط ب'),
        ('متقدم أ','متقدم أ'),
        ('متقدم ب','متقدم ب'),
    )
    time = (
        ('بعد جلسة الصفا','بعد جلسة الصفا'),
    )
    position = (
        ('حرم رئيسي','حرم رئيسي'),
        ('توسعة حرم رئيسي','توسعة حرم رئيسي'),
        ('تحت السدة','تحت السدة'),
        ('توسعة مكتبة','توسعة مكتبة'),
        ('قبو','قبو'),
    )
    session_id = models.IntegerField(primary_key=True)
    session_number = models.IntegerField()
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE)
    level_id = models.CharField(max_length=50, null=True, choices=level)
    position_id = models.CharField(max_length=50, null=True, choices=position)
    time_id = models.CharField(max_length=50, null=True, choices=time)
    teacher_id = models.ForeignKey(Person, null=True, on_delete=models.SET_NULL)
    create_date = models.DateField(auto_now_add=True, null=True)
    def __str__(self):
        return f'{self.session_id}'

class Session_Student(models.Model):
    id = models.IntegerField(primary_key=True)
    session_id = models.ForeignKey(Session, on_delete=models.CASCADE)
    student_id = models.ForeignKey(Person, on_delete=models.CASCADE)
    create_date = models.DateField(auto_now_add=True, null=True)
    def __str__(self):
        return f'{self.id}'

class Attendance(models.Model):
    attendance_id = models.IntegerField(primary_key=True)
    person_id = models.ForeignKey(Person, on_delete=models.CASCADE)
    session_id = models.ForeignKey(Session, on_delete=models.CASCADE)
    day = models.DateField()
    status = models.BooleanField()
    create_date = models.DateField(auto_now_add=True, null=True)
    def __str__(self):
        return f'{self.day}'

class Exam(models.Model):
    exam_type = (
        ('نظري','نظري'),
        ('عملي','عملي'),
    )
    exam_time = (
        ('الامتحان الأول','الامتحان الأول'),
        ('التكميلي','التكميلي'),
        ('الاعادة','الاعادة'),
    )
    exam_id = models.IntegerField(primary_key=True)
    type_id = models.CharField(max_length=50, null=True, choices=exam_type)
    time_id = models.CharField(max_length=50, null=True, choices=exam_time)
    student_id = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='student_id')
    teacher_id = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='teacher_id', null=True)
    session_id = models.ForeignKey(Session, on_delete=models.CASCADE)
    mark = models.FloatField(null=True)
    create_date = models.DateField(auto_now_add=True, null=True)
    def __str__(self):
        return f'{self.mark}'

class Result(models.Model):
    result = (
        ('إعادة','إعادة'),
        ('ناجح','ناجح'),
        ('نجاح شرطي','نجاح شرطي')
    )
    result_id = models.IntegerField(primary_key=True)
    student_id = models.ForeignKey(Person, on_delete=models.CASCADE)
    session_id = models.ForeignKey(Session, on_delete=models.CASCADE)
    attendance = models.FloatField(null=True)
    theoretical_mark = models.FloatField(null=True)
    practical_mark = models.FloatField(null=True)
    result = models.CharField(max_length=50, null=True, choices=result)
    create_date = models.DateField(auto_now_add=True, null=True)
    def __str__(self):
        return f'{self.result}'