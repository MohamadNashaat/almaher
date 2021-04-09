from django.db import models

class Person_Type(models.Model):
    per_type_id = models.AutoField(primary_key=True)
    type_name = models.CharField(max_length=120)
    def __str__(self):
        return self.type_name

class Person(models.Model):
    person_id = models.AutoField(primary_key=True)
    type_id = models.ForeignKey(Person_Type, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=120)
    last_name = models.CharField(max_length=120)
    father_name = models.CharField(max_length=120)
    home_number = models.CharField(max_length=120)
    phone_number = models.CharField(max_length=120)
    job = models.CharField(max_length=120)
    address = models.CharField(max_length=120)
    bdate = models.DateField()
    level_id = models.ForeignKey('Level', on_delete=models.CASCADE, null=True)
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
    session_number = models.IntegerField()
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE)
    level_id = models.ForeignKey(Level, on_delete=models.CASCADE)
    position_id = models.ForeignKey(Position, on_delete=models.CASCADE)
    time_id = models.ForeignKey(Time, on_delete=models.CASCADE)
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