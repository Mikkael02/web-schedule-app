from .models import Schedule, Course, Group, Teacher, Room
from TimeConfiguration.models import TimeConfiguration
from django import forms
from .models import Schedule
from department.models import Department

class ScheduleForm(forms.ModelForm):
    class Meta:
        model = Schedule
        fields = ['course', 'group', 'room', 'teacher', 'week_type', 'day_of_week', 'start_time', 'end_time']

    def __init__(self, *args, **kwargs):
        institution = kwargs.pop('institution', None)
        super().__init__(*args, **kwargs)
        if institution:
            self.fields['course'].queryset = Course.objects.filter(institution=institution)
            self.fields['group'].queryset = Group.objects.filter(institution=institution)
            self.fields['room'].queryset = institution.rooms.all()
            self.fields['teacher'].queryset = institution.teachers.all()

class ManualScheduleForm(forms.ModelForm):
    start_time = forms.ChoiceField(label='Godzina rozpoczęcia', choices=[])

    class Meta:
        model = Schedule
        fields = ['group', 'course', 'teacher', 'room', 'week_type', 'day_of_week', 'start_time']

    def __init__(self, *args, institution=None, start_times=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['group'].queryset = Group.objects.filter(institution=institution)
        self.fields['course'].queryset = Course.objects.filter(institution=institution)
        self.fields['teacher'].queryset = Teacher.objects.filter(institution=institution)
        self.fields['room'].queryset = Room.objects.filter(institution=institution)
        self.fields['start_time'].choices = [(t.strftime('%H:%M'), t.strftime('%H:%M')) for t in start_times]