from .models import Schedule, Course, Group
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

class CourseAssignmentForm(forms.Form):
    def __init__(self, *args, **kwargs):
        institution_type = kwargs.pop('institution_type')
        super().__init__(*args, **kwargs)
        self.fields['courses'] = forms.ModelMultipleChoiceField(
            queryset=Course.objects.filter(institution__type=institution_type),
            widget=forms.CheckboxSelectMultiple
        )
        self.fields['weekly_count'] = forms.FloatField(min_value=0.5, step=0.5)

    def save_assignments(self, institution):
        # Logika przypisywania kursów do grup/kierunków
        pass
