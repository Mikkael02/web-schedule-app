from django.db import models
from institutions.models import Institution
from department.models import Department
from group.models import Group
from course.models import Course

class SubjectFrequency(models.Model):
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, null=True, blank=True)  # Dla primary
    department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True, blank=True)  # Dla secondary/higher
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    frequency = models.FloatField(default=0)

    class Meta:
        unique_together = ('institution', 'group', 'department', 'course')

    def __str__(self):
        return f"{self.group or self.department} - {self.course} ({self.frequency})"
