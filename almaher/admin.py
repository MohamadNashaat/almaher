from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(Person)
admin.site.register(Course)
admin.site.register(Session)
admin.site.register(Session_Student)
admin.site.register(Attendance)
admin.site.register(Exam)
