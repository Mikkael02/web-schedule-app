from django import forms
from .models import RoomType

class RoomTypeForm(forms.ModelForm):
    class Meta:
        model = RoomType
        fields = ['name']
