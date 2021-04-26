# Generated by Django 3.1.7 on 2021-04-24 04:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('almaher', '0013_auto_20210424_0404'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='exam',
            name='exam_time_id',
        ),
        migrations.RemoveField(
            model_name='exam',
            name='exam_type_id',
        ),
        migrations.RemoveField(
            model_name='exam',
            name='session_id',
        ),
        migrations.RemoveField(
            model_name='exam',
            name='student_id',
        ),
        migrations.RemoveField(
            model_name='exam',
            name='teacher_id',
        ),
        migrations.DeleteModel(
            name='Person_Type',
        ),
        migrations.RemoveField(
            model_name='session',
            name='position_id',
        ),
        migrations.RemoveField(
            model_name='session',
            name='time_id',
        ),
        migrations.AlterField(
            model_name='session',
            name='level_id',
            field=models.CharField(choices=[('مبتدأ أ', 'مبتدأ أ'), ('مبتدأ ب', 'مبتدأ ب'), ('متوسط أ', 'متوسط أ'), ('متوسط ب', 'متوسط ب'), ('متقدم أ', 'متقدم أ'), ('متقدم ب', 'متقدم ب')], max_length=50, null=True),
        ),
        migrations.DeleteModel(
            name='Exam',
        ),
        migrations.DeleteModel(
            name='Exam_Time',
        ),
        migrations.DeleteModel(
            name='Exam_Type',
        ),
        migrations.DeleteModel(
            name='Level',
        ),
        migrations.DeleteModel(
            name='Position',
        ),
        migrations.DeleteModel(
            name='Time',
        ),
    ]