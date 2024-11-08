from django.forms import ModelForm
from .models import Schedule

class ScheduleForm(ModelForm):
    class Meta:
        model = Schedule
        fields = ['course', 'group', 'room', 'teacher', 'week_type', 'day_of_week', 'start_time', 'end_time', 'institution']
