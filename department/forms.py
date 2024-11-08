from django.forms import ModelForm
from .models import Department

class FacultyForm(ModelForm):
    class Meta:
        model = Department
        fields = ['name', 'faculty']
