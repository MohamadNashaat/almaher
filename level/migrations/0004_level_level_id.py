# Generated by Django 3.1.7 on 2021-07-21 07:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('level', '0003_remove_level_level_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='level',
            name='level_id',
            field=models.IntegerField(null=True),
        ),
    ]
