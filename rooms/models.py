from django.db import models

class Room(models.Model):
    ROOM_TYPES = (
        ('lecture', 'Wykład'),
        ('lab', 'Laboratorium'),
        ('sport', 'Sala sportowa'),
        # WRÓCIĆ!!! DODAĆ EWENTUALNIE INNE TYPY
    )
    name = models.CharField(max_length=100)
    capacity = models.IntegerField()
    room_type = models.CharField(max_length=10, choices=ROOM_TYPES)

    def __str__(self):
        return f"{self.name} ({self.room_type})"
