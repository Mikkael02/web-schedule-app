from django.db import models

class Teacher(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    # Można ewentualnie dodać później model Specialization i połączyć przez ManyToManyField!!! WRÓĆ!!

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
