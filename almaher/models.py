from django.db import models

class Person_Type(models.Model):
    per_type_id = models.IntegerField(primary_key=True)
    type_name = models.CharField(max_length=120)
    def __str__(self):
        return self.type_name
    # per_type_id = 1 ==> Teacher
    # per_type_id = 2 ==> Student

class Person(models.Model):
    person_id = models.AutoField(primary_key=True)
    person_type_id = models.ForeignKey(Person_Type, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=120)
    last_name = models.CharField(max_length=120)
    father_name = models.CharField(max_length=120)
    home_number = models.CharField(max_length=120)
    phone_number = models.CharField(max_length=120)
    job = models.CharField(max_length=120)
    address = models.CharField(max_length=120)
    bdate = models.DateField()
    level_id = models.ForeignKey('Level', on_delete=models.CASCADE, null=True)
    status = models.BooleanField(default=True)
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

class Level(models.Model):
    level_id = models.AutoField(primary_key=True)
    level_name = models.CharField(max_length=120)
    def __str__(self):
        return self.level_name

class Position(models.Model):
    position_id = models.AutoField(primary_key=True)
    position_name = models.CharField(max_length=120)
    def __str__(self):
        return self.position_name

class Time(models.Model):
    time_id = models.AutoField(primary_key=True)
    time_name = models.CharField(max_length=120)
    def __str__(self):
        return self.time_name

class Session(models.Model):
    session_id = models.AutoField(primary_key=True)
    session_number = models.IntegerField(unique=True)
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE)
    level_id = models.ForeignKey(Level, on_delete=models.CASCADE)
    position_id = models.ForeignKey(Position, null=True, on_delete=models.CASCADE)
    time_id = models.ForeignKey(Time, null=True, on_delete=models.CASCADE)
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

class Exam_Type(models.Model):
    exam_type_id = models.AutoField(primary_key=True)
    exam_type_name = models.CharField(max_length=120)
    def __str__(self):
        return f'{self.exam_type_name}'
    #exam_type_id = 1 ==> نظري
    #exam_type_id = 2 ==> عملي

class Exam_Time(models.Model):
    exam_time_id = models.AutoField(primary_key=True)
    exam_time_name = models.CharField(max_length=120)
    def __str__(self):
        return f'{self.exam_time_name}'
    #exam_time_id = 1 ==> الامتحان الأول
    #exam_time_id = 2 ==> التكميلي
    #exam_time_id = 3 ==> الاعادة 

class Exam(models.Model):
    exam_id = models.AutoField(primary_key=True)
    exam_type_id = models.ForeignKey(Exam_Type, on_delete=models.CASCADE)
    exam_time_id = models.ForeignKey(Exam_Time, on_delete=models.CASCADE)
    student_id = models.ForeignKey(Person, on_delete=models.CASCADE)
    teacher_id = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='teacher_id')
    session_id = models.ForeignKey(Session, on_delete=models.CASCADE)
    first_mark = models.FloatField(null=True)
    second_mark = models.FloatField(null=True)
    result = models.FloatField()