from django.contrib import admin

# Register your models here.

from .models import *
admin.site.register(Person_Type)
admin.site.register(Person)