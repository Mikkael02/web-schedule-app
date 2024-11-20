from django import forms
from django.forms import modelformset_factory
from .models import SubjectFrequency
from group.models import Group
from department.models import Department
from course.models import Course

class SubjectFrequencyForm(forms.ModelForm):
    class Meta:
        model = SubjectFrequency
        fields = ['group', 'department', 'course', 'frequency']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['group'].widget = forms.HiddenInput()
        self.fields['department'].widget = forms.HiddenInput()

SubjectFrequencyFormSet = modelformset_factory(
    SubjectFrequency,
    form=SubjectFrequencyForm,
    extra=10,
)
