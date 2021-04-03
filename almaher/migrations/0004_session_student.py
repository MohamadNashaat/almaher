# Generated by Django 3.1.7 on 2021-03-29 17:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('almaher', '0003_remove_session_student_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='Session_Student',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('session_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='almaher.session')),
                ('student_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='almaher.person')),
            ],
        ),
    ]