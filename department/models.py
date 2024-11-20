from django.db import models
from faculty.models import Faculty
from institutions.models import Institution

class Department(models.Model):
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, related_name='departments', null=True, blank=True)
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE, related_name='departments', null=True, blank=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

