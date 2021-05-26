from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name=''),
    path('login', views.user_login, name='login'),
    path('logout', views.user_logout, name='logout'),
    path('blank', views.blank, name='blank'),
    path('404', views.pg_404, name='404'),
]