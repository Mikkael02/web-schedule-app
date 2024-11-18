import json
from django import forms
from .models import TimeConfiguration
from django.core.exceptions import ValidationError

class TimeConfigurationForm(forms.ModelForm):
    class Meta:
        model = TimeConfiguration
        fields = ['start_time', 'lesson_duration', 'break_type', 'break_duration', 'custom_breaks']

    def clean(self):
        cleaned_data = super().clean()
        break_type = cleaned_data.get('break_type')
        break_duration = cleaned_data.get('break_duration')
        custom_breaks = cleaned_data.get('custom_breaks')

        if break_type == 'same' and not break_duration:
            raise ValidationError("Długość przerwy jest wymagana dla przerw o tej samej długości.")

        if break_type == 'custom':
            if not custom_breaks:
                raise ValidationError("Musisz określić długości przerw dla przerw o różnej długości.")
            if isinstance(custom_breaks, str):
                try:
                    custom_breaks = json.loads(custom_breaks)
                except json.JSONDecodeError:
                    raise ValidationError("Custom breaks must be a valid JSON object.")
            if not isinstance(custom_breaks, dict):
                raise ValidationError("Custom breaks must be a valid JSON object.")

            for key, value in custom_breaks.items():
                if not (isinstance(key, str) and isinstance(value, str)):
                    raise ValidationError("Keys and values in custom breaks must be strings representing times.")

            cleaned_data['custom_breaks'] = custom_breaks  # Ensure data is saved as dict

        return cleaned_data
