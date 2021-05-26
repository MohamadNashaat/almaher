from django.db import models

# Create your models here.

class Time(models.Model):
    time_name = models.CharField(max_length=50, primary_key=True)
    create_date = models.DateField(auto_now_add=True, null=True)
    def __str__(self):
        return self.time_name