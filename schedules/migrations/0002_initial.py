# Generated by Django 5.1.3 on 2024-11-07 19:25

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('schedules', '0001_initial'),
        ('teachers', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='schedule',
            name='teacher',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='teachers.teacher'),
        ),
    ]