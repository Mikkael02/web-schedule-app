from django import forms
from .models import Schedule, Group, Course, Teacher, Room

class ManualScheduleForm(forms.ModelForm):
    group = forms.ModelMultipleChoiceField(
        queryset=Group.objects.none(),
        widget=forms.CheckboxSelectMultiple,
        label="Wybierz grupy"
    )
    start_time = forms.ChoiceField(label='Godzina rozpoczęcia', choices=[])

    class Meta:
        model = Schedule
        fields = ['group', 'course', 'teacher', 'room', 'week_type', 'day_of_week', 'start_time']

    def __init__(self, *args, institution=None, start_times=None, **kwargs):
        super().__init__(*args, **kwargs)
        if institution:
            self.fields['group'].queryset = Group.objects.filter(institution=institution)
            self.fields['course'].queryset = Course.objects.filter(institution=institution)
            self.fields['teacher'].queryset = Teacher.objects.filter(institution=institution)
            self.fields['room'].queryset = Room.objects.filter(institution=institution)
        if start_times:
            self.fields['start_time'].choices = [(t.strftime('%H:%M'), t.strftime('%H:%M')) for t in start_times]
