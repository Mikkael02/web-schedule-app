from django.db import models

class Course(models.Model):
    COURSE_TYPES = (
        ('lecture', 'Wykład'),
        ('lab', 'Laboratorium'),
        ('seminar', 'Seminarium'),
        # Dodaj więcej typów kursów zgodnie z potrzebami
    )

    name = models.CharField(max_length=100)
    course_type = models.CharField(max_length=50, choices=COURSE_TYPES, default='lecture', blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.course_type if self.course_type else 'No Type'})"
