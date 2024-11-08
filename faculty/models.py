from django.db import models
from institutions.models import Institution

class Faculty(models.Model):
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE, related_name='faculties')
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
