from django.db import models
from institutions.models import Institution
from room_types.models import RoomType  # Typ kursu
from equipment.models import Equipment  # Wymagane wyposażenie

class Course(models.Model):
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE, related_name='courses', null=True)
    name = models.CharField(max_length=100)
    course_type = models.ForeignKey(RoomType, on_delete=models.SET_NULL, null=True, blank=True, help_text="Opcjonalny typ zajęć")
    equipment = models.ManyToManyField(Equipment, blank=True, help_text="Wybierz wymagane wyposażenie dla zajęć")

    def __str__(self):
        equipment_list = ', '.join(eq.name for eq in self.equipment.all())
        return f"{self.name} ({self.course_type.name if self.course_type else 'Brak typu'}) - Sprzęt: {equipment_list if equipment_list else 'Brak'}"
