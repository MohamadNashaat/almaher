# Generated by Django 3.1.7 on 2021-03-27 19:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('almaher', '0002_auto_20210327_1908'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendance',
            name='status',
            field=models.BooleanField(default=False),
        ),
    ]
