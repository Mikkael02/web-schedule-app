# Generated by Django 4.2.11 on 2024-05-06 06:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('department', '0002_initial'),
        ('group', '0006_alter_group_department'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='department',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='groups', to='department.department'),
        ),
    ]