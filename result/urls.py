from django.urls import path
from . import views

urlpatterns = [
    path('', views.result, name='result'),
    path('generate', views.generate_result, name='generate_result'),  
    path('pass', views.student_pass, name='student_pass'),

    path('set_result_type', views.set_result_type, name='set_result_type'),
]