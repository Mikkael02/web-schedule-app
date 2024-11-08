from django.db import models
from rooms.models import Room
from teachers.models import Teacher
from course.models import Course
from group.models import Group
from institutions.models import Institution

def get_default_group():
    default_group = Group.objects.get_or_create(name="Default Group")[0]
    return default_group.id

class Schedule(models.Model):
    WEEK_TYPE_CHOICES = (
        ('weekly', 'Co tydzień'),
        ('even', 'Tygodnie parzyste'),
        ('odd', 'Tygodnie nieparzyste'),
    )
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE, related_name='schedules', null=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, default=get_default_group)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    week_type = models.CharField(max_length=10, choices=WEEK_TYPE_CHOICES, default='weekly')
    day_of_week = models.CharField(
        max_length=10,
        choices=[
            ('Monday', 'Monday'),
            ('Tuesday', 'Tuesday'),
            ('Wednesday', 'Wednesday'),
            ('Thursday', 'Thursday'),
            ('Friday', 'Friday'),
            ('Saturday', 'Saturday'),
            ('Sunday', 'Sunday')
        ],
        default='Monday'
    )
    start_time = models.TimeField(default='14:00')
    end_time = models.TimeField(default='15:30')

    def __str__(self):
        return f"{self.course} in {self.room} by {self.teacher} for {self.group} on {self.day_of_week} from {self.start_time} to {self.end_time}"
