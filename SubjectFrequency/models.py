from django.db import models
from institutions.models import Institution
from department.models import Department
from group.models import Group
from course.models import Course

class SubjectFrequency(models.Model):
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, null=True, blank=True)  # Pojedyncza grupa
    department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True, blank=True)  # Dla secondary/higher
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    frequency = models.FloatField(default=0)
    shared_groups = models.ManyToManyField(Group, related_name="shared_subjects", blank=True)  # Grupy współdzielące zajęcia

    class Meta:
        unique_together = ('institution', 'group', 'department', 'course')

    def __str__(self):
        shared_info = f" + {self.shared_groups.count()} shared groups" if self.shared_groups.exists() else ""
        return f"{self.group or self.department} - {self.course} ({self.frequency}){shared_info}"

