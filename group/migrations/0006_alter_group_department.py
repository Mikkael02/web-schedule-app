# Generated by Django 4.2.11 on 2024-05-06 05:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('group', '0005_remove_group_faculty_alter_group_department'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='department',
            field=models.CharField(blank=True, help_text='Kierunek, jeśli dotyczy', max_length=100, null=True),
        ),
    ]
