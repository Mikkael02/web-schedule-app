from django.db import models

class Group(models.Model):
    name = models.CharField(max_length=100)
    department = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.department if self.department else 'No Department'})"
