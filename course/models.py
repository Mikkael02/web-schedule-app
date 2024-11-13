from django.db import models
from institutions.models import Institution
from room_types.models import RoomType  # Typ kursu
from equipment.models import Equipment  # Wymagane wyposażenie

class Course(models.Model):
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE, related_name='courses', null=True)
    name = models.CharField(max_length=100)
    room_types = models.ManyToManyField(RoomType, blank=True, help_text="Wybierz typy zajęć")  # ManyToManyField
    equipment = models.ManyToManyField(Equipment, blank=True, help_text="Wybierz wymagane wyposażenie dla zajęć")

    def __str__(self):
        return f"{self.name} - Typy: {', '.join(rt.name for rt in self.room_types.all()) if self.room_types.exists() else 'Brak'}"
