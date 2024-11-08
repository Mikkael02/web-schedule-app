from django.db import models
from institutions.models import Institution
from room_types.models import RoomType  # Nowy model RoomType
from equipment.models import Equipment  # Nowy model Equipment

class Room(models.Model):
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE, related_name='rooms', null=True)
    name = models.CharField(max_length=100)
    capacity = models.IntegerField()
    room_types = models.ManyToManyField(RoomType, blank=True, help_text="Wybierz typy, do których sala się nadaje")
    equipment = models.ManyToManyField(Equipment, blank=True, help_text="Wybierz sprzęt dostępny w sali")

    def __str__(self):
        room_types = ', '.join(rt.name for rt in self.room_types.all())
        return f"{self.name} - {room_types if room_types else 'Brak typu'}"
