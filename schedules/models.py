from django.db import models
from rooms.models import Room
from teachers.models import Teacher

class Schedule(models.Model):
    course = models.CharField(max_length=200)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    time_slot = models.DateTimeField()

    def __str__(self):
        return f"{self.course} - {self.time_slot}"
