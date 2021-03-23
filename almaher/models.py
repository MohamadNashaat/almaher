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

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


