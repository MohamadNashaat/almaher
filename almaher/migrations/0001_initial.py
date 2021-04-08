# Generated by Django 3.1.7 on 2021-04-08 11:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('course_id', models.AutoField(primary_key=True, serialize=False)),
                ('course_name', models.CharField(max_length=120)),
                ('start_date', models.DateField(null=True)),
                ('end_date', models.DateField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Level',
            fields=[
                ('level_id', models.AutoField(primary_key=True, serialize=False)),
                ('level_name', models.CharField(max_length=120)),
            ],
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('person_id', models.AutoField(primary_key=True, serialize=False)),
                ('first_name', models.CharField(max_length=120)),
                ('last_name', models.CharField(max_length=120)),
                ('father_name', models.CharField(max_length=120)),
                ('home_number', models.CharField(max_length=120)),
                ('phone_number', models.CharField(max_length=120)),
                ('job', models.CharField(max_length=120)),
                ('address', models.CharField(max_length=120)),
                ('bdate', models.DateField()),
                ('create_date', models.DateField(auto_now_add=True, null=True)),
                ('level_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='almaher.level')),
            ],
        ),
        migrations.CreateModel(
            name='Person_Type',
            fields=[
                ('per_type_id', models.AutoField(primary_key=True, serialize=False)),
                ('type_name', models.CharField(max_length=120)),
            ],
        ),
        migrations.CreateModel(
            name='Position',
            fields=[
                ('position_id', models.AutoField(primary_key=True, serialize=False)),
                ('position_name', models.CharField(max_length=120)),
            ],
        ),
        migrations.CreateModel(
            name='Session',
            fields=[
                ('session_id', models.AutoField(primary_key=True, serialize=False)),
                ('session_number', models.IntegerField()),
                ('course_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='almaher.course')),
                ('level_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='almaher.level')),
                ('position_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='almaher.position')),
                ('teacher_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='almaher.person')),
            ],
        ),
        migrations.CreateModel(
            name='Time',
            fields=[
                ('time_id', models.AutoField(primary_key=True, serialize=False)),
                ('time_name', models.CharField(max_length=120)),
            ],
        ),
        migrations.CreateModel(
            name='Session_Student',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('session_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='almaher.session')),
                ('student_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='almaher.person')),
            ],
        ),
        migrations.AddField(
            model_name='session',
            name='time_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='almaher.time'),
        ),
        migrations.AddField(
            model_name='person',
            name='type_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='almaher.person_type'),
        ),
        migrations.CreateModel(
            name='Attendance',
            fields=[
                ('attendance_id', models.AutoField(primary_key=True, serialize=False)),
                ('day', models.DateField()),
                ('status', models.BooleanField()),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='almaher.course')),
                ('person_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='almaher.person')),
            ],
        ),
    ]
