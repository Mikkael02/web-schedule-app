from django.contrib.auth.models import User
from django.db import models

class Institution(models.Model):
    TYPE_CHOICES = (
        ('primary', 'Szkoła Podstawowa'),
        ('secondary', 'Szkoła Średnia'),
        ('higher', 'Szkoła Wyższa'),
    )
    name = models.CharField(max_length=200)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    location = models.CharField(max_length=300, blank=True, null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='institutions', blank=True, null=True)
    logo = models.ImageField(upload_to='institution_logos/', blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.get_type_display()})"
