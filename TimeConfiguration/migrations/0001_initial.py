# Generated by Django 5.1.3 on 2024-11-15 13:57

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('institutions', '0003_institution_logo'),
    ]

    operations = [
        migrations.CreateModel(
            name='TimeConfiguration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.TimeField(default='08:00', help_text='Czas rozpoczęcia pierwszych zajęć.')),
                ('lesson_duration', models.DurationField(help_text='Czas trwania pojedynczej lekcji (np. 45 minut).')),
                ('break_type', models.CharField(choices=[('same', 'Przerwy o tej samej długości'), ('custom', 'Przerwy o różnej długości')], default='same', max_length=10)),
                ('break_duration', models.DurationField(blank=True, help_text='Długość przerw, jeśli są jednakowe.', null=True)),
                ('custom_breaks', models.JSONField(blank=True, help_text="Długości przerw dla każdej lekcji w formacie JSON. Przykład: {1: '00:15', 2: '00:10'}", null=True)),
                ('institution', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='time_configuration', to='institutions.institution')),
            ],
        ),
    ]
