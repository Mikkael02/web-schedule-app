from django.db import models
from institutions.models import Institution
from department.models import Department

class Group(models.Model):
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE, related_name='groups', null=True)
    name = models.CharField(max_length=100)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='groups', null=True)
    size = models.IntegerField(default=20, help_text="Liczba osób w grupie")
    LEVEL_CHOICES = [
        ('1', 'Klasa 1'), ('2', 'Klasa 2'), ('3', 'Klasa 3'), ('4', 'Klasa 4'),
        ('5', 'Klasa 5'), ('6', 'Klasa 6'), ('7', 'Klasa 7'), ('8', 'Klasa 8'),
        ('S1', 'Semestr 1'), ('S2', 'Semestr 2'), ('S3', 'Semestr 3'), ('S4', 'Semestr 4'),
        ('S5', 'Semestr 5'), ('S6', 'Semestr 6'), ('S7', 'Semestr 7'), ('S8', 'Semestr 8'),
        ('S9', 'Semestr 9'), ('S10', 'Semestr 10'), ('S11', 'Semestr 11'), ('S12', 'Semestr 12')
    ]
    level = models.CharField(max_length=3, choices=LEVEL_CHOICES, default='1',  help_text="Klasa lub semestr, do którego grupa należy")

    def __str__(self):
        return f"{self.name} - {self.department if self.department else 'Brak kierunku'} - {self.get_level_display()}"
