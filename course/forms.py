# course/forms.py
from django import forms
from .models import Course
from room_types.models import RoomType
from equipment.models import Equipment

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['name', 'course_type', 'equipment']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nazwa zajęć'}),
            'course_type': forms.Select(attrs={'class': 'form-control'}),
            'equipment': forms.SelectMultiple(attrs={'class': 'form-control'}),
        }
        labels = {
            'name': 'Nazwa zajęć',
            'course_type': 'Typ zajęć',
            'equipment': 'Wymagane wyposażenie',
        }
