from django.db import models

class RoomType(models.Model):
    TYPE_CHOICES = (
        ('lecture', 'Wykład'),
        ('lab', 'Laboratorium'),
        ('seminar', 'Seminarium'),
        ('project', 'Projekt'),
        ('exercises', 'Ćwiczenia'),
        ('sport', 'Ćwiczenia sportowe'),
    )
    type = models.CharField(max_length=50, choices=TYPE_CHOICES, unique=True)

    def __str__(self):
        return self.get_type_display()

class Equipment(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Room(models.Model):
    name = models.CharField(max_length=100)
    capacity = models.IntegerField()
    room_types = models.ManyToManyField(RoomType, blank=True, help_text="Wybierz typy, do których sala się nadaje")
    equipment = models.ManyToManyField(Equipment, blank=True, help_text="Wybierz sprzęt dostępny w sali")

    def __str__(self):
        room_types = ', '.join(type.get_type_display() for type in self.room_types.all())
        return f"{self.name} - {room_types if room_types else 'No Type'}"
