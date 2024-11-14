from django.forms import ModelForm
from .models import Institution
from django import forms
from group.models import Group
from teachers.models import Teacher
from course.models import Course
from equipment.models import Equipment
from rooms.models import Room, RoomType
from department.models import Department
from faculty.models import Faculty

class InstitutionForm(ModelForm):
    class Meta:
        model = Institution
        fields = ['name', 'type', 'location']

class RoomForm(forms.ModelForm):
    add_room_type = forms.CharField(required=False, label="Dodaj nowy typ sali")
    add_equipment = forms.CharField(required=False, label="Dodaj nowe wyposażenie")

    class Meta:
        model = Room
        fields = ['name', 'capacity', 'room_types', 'equipment']
        widgets = {
            'room_types': forms.CheckboxSelectMultiple(),
            'equipment': forms.CheckboxSelectMultiple(),
        }

    def save(self, commit=True):
        room = super().save(commit=False)

        # Dynamiczne dodawanie typu sali
        new_room_type = self.cleaned_data.get('add_room_type')
        if new_room_type:
            room_type, created = RoomType.objects.get_or_create(name=new_room_type)
            room.room_types.add(room_type)

        # Dynamiczne dodawanie wyposażenia
        new_equipment = self.cleaned_data.get('add_equipment')
        if new_equipment:
            equipment, created = Equipment.objects.get_or_create(name=new_equipment)
            room.equipment.add(equipment)

        if commit:
            room.save()
            self.save_m2m()
        return room

class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['name', 'size', 'level', 'department']
        widgets = {
            'level': forms.Select(),
        }

    def __init__(self, *args, **kwargs):
        institution_type = kwargs.pop('institution_type', None)
        super().__init__(*args, **kwargs)

        # Ukryj department, jeśli instytucja jest typu primary
        if institution_type == 'primary':
            self.fields.pop('department')

class TeacherForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ['first_name', 'last_name', 'title', 'email', 'courses']
        widgets = {
            'email': forms.EmailInput(),
            'courses': forms.CheckboxSelectMultiple(),
        }


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['name', 'room_types', 'equipment']  # Upewnij się, że 'room_types' jest tutaj
        widgets = {
            'room_types': forms.CheckboxSelectMultiple(),
            'equipment': forms.CheckboxSelectMultiple(),
        }

    def save(self, commit=True):
        course = super().save(commit=False)

        # Dynamiczne dodawanie wyposażenia
        new_equipment = self.cleaned_data.get('add_equipment')
        if new_equipment:
            equipment, created = Equipment.objects.get_or_create(name=new_equipment)
            course.equipment.add(equipment)

        if commit:
            course.save()
            self.save_m2m()
        return course

class DepartmentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        institution_type = kwargs.pop('institution_type', None)
        super().__init__(*args, **kwargs)

        if institution_type == 'higher':
            self.fields['faculty'].queryset = Faculty.objects.all()
        else:
            self.fields.pop('faculty', None)  # Usuwamy pole dla secondary

    class Meta:
        model = Department
        fields = ['name', 'faculty']  # Faculty będzie usunięte dynamicznie, jeśli nie jest potrzebne
