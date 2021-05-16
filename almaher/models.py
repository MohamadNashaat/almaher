from django.db import models

class Level(models.Model):
    level_name = models.CharField(max_length=50, primary_key=True)
    create_date = models.DateField(auto_now_add=True, null=True)
    def __str__(self):
        return self.level_name

class Position(models.Model):
    position_name = models.CharField(max_length=50, primary_key=True)
    create_date = models.DateField(auto_now_add=True, null=True)
    def __str__(self):
        return self.position_name

class Time(models.Model):
    time_name = models.CharField(max_length=50, primary_key=True)
    create_date = models.DateField(auto_now_add=True, null=True)
    def __str__(self):
        return self.time_name

class Person(models.Model):
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
    level_id = models.ForeignKey(Level, on_delete=models.CASCADE)
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
    num_of_session = models.IntegerField(null=True)
    create_date = models.DateField(auto_now_add=True, null=True)
    def __str__(self):
        return self.course_name

class Session(models.Model):
    session_id = models.IntegerField(primary_key=True)
    session_number = models.IntegerField()
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE)
    level_id = models.ForeignKey(Level, on_delete=models.CASCADE)
    position_id = models.ForeignKey(Position, on_delete=models.CASCADE)
    time_id = models.ForeignKey(Time, on_delete=models.CASCADE)
    teacher_id = models.ForeignKey(Person, null=True, on_delete=models.CASCADE)
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
    student_id = models.ForeignKey(Person, on_delete=models.CASCADE)
    #teacher_id = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='teacher_id', null=True)
    session_id = models.ForeignKey(Session, on_delete=models.CASCADE)
    mark = models.IntegerField(null=True)
    create_date = models.DateField(auto_now_add=True, null=True)
    def __str__(self):
        return f'{self.mark}'

class Result(models.Model):
    result_type = (
        ('ناجح','ناجح'),
        ('نجاح شرطي','نجاح شرطي'),
        ('إعادة','إعادة'),
    )
    result_id = models.IntegerField(primary_key=True)
    student_id = models.ForeignKey(Person, on_delete=models.CASCADE)
    session_id = models.ForeignKey(Session, on_delete=models.CASCADE)
    attendance = models.FloatField(null=True)
    theoretical_mark = models.FloatField(null=True)
    practical_mark = models.FloatField(null=True)
    result = models.CharField(max_length=50, null=True, choices=result_type)
    create_date = models.DateField(auto_now_add=True, null=True)
    def __str__(self):
        return f'{self.result}'