# Generated by Django 3.1.7 on 2021-04-24 04:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('almaher', '0014_auto_20210424_0429'),
    ]

    operations = [
        migrations.AddField(
            model_name='session',
            name='position_id',
            field=models.CharField(choices=[('حرم رئيسي', 'حرم رئيسي'), ('توسعة حرم رئيسي', 'توسعة حرم رئيسي'), ('تحت السدة', 'تحت السدة'), ('توسعة مكتبة', 'توسعة مكتبة'), ('قبو', 'قبو')], max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='session',
            name='time_id',
            field=models.CharField(choices=[('بعد جلسة الصفا', 'بعد جلسة الصفا')], max_length=50, null=True),
        ),
    ]