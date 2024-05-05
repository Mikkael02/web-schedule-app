from django.db import models
from course.models import Course

class Teacher(models.Model):
    TITLES = (
        ('inż.', 'inż.'),
        ('mgr inż.', 'mgr inż.'),
        ('dr inż.', 'dr inż.'),
        ('dr hab. inż.', 'dr hab. inż.'),
        ('prof. dr hab. inż.', 'prof. dr hab. inż.'),
    )
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    title = models.CharField(max_length=50, choices=TITLES, default='mgr inż.')
    courses = models.ManyToManyField(Course, blank=True, help_text="Kursy, które nauczyciel może prowadzić")

    def __str__(self):
        return f"{self.title} {self.first_name} {self.last_name}"
