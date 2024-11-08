from django import forms
from .models import Room
from room_types.models import RoomType
from equipment.models import Equipment

class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['name', 'capacity', 'room_types', 'equipment']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nazwa sali'}),
            'capacity': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Pojemność sali'}),
            'room_types': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'equipment': forms.SelectMultiple(attrs={'class': 'form-control'}),
        }
        labels = {
            'name': 'Nazwa',
            'capacity': 'Pojemność',
            'room_types': 'Typy sali',
            'equipment': 'Wyposażenie',
        }
