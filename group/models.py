from django.db import models

class Group(models.Model):
    name = models.CharField(max_length=100)
    department = models.CharField(max_length=100, blank=True, null=True)
    size = models.IntegerField(default=20, help_text="Liczba osób w grupie")

    def __str__(self):
        return f"{self.name} ({self.department if self.department else 'No Department'})"
