from django.db import models
from datetime import timedelta
from institutions.models import Institution
from django.core.exceptions import ValidationError

class TimeConfiguration(models.Model):
    BREAK_TYPE_CHOICES = (
        ('same', 'Przerwy o tej samej długości'),
        ('custom', 'Przerwy o różnej długości'),
    )

    institution = models.OneToOneField(Institution, on_delete=models.CASCADE, related_name='time_configuration')
    start_time = models.TimeField(default='08:00', help_text="Czas rozpoczęcia pierwszych zajęć.")
    end_time = models.TimeField(default='20:00', help_text="Czas zakończenia ostatnich zajęć.")  # Nowe pole
    lesson_duration = models.DurationField(default=timedelta(minutes=45),
                                           help_text="Czas trwania pojedynczej lekcji (np. 45 minut).")
    break_type = models.CharField(max_length=10, choices=BREAK_TYPE_CHOICES, default='same')
    break_duration = models.DurationField(null=True, blank=True, default=timedelta(minutes=15),
                                          help_text="Długość przerw, jeśli są jednakowe.")
    custom_breaks = models.JSONField(
        null=True,
        blank=True,
        help_text="Długości przerw dla każdej lekcji w formacie JSON. Przykład: {1: '00:15:00', 2: '00:10:00'}"
    )

    def clean(self):
        if self.break_type == 'same' and not self.break_duration:
            raise ValidationError("Dla przerw o tej samej długości musisz podać wartość break_duration.")
        if self.break_type == 'custom' and not self.custom_breaks:
            raise ValidationError("Dla przerw o różnej długości musisz podać wartość custom_breaks.")

        if self.custom_breaks:
            try:
                parsed_breaks = {int(k): timedelta(seconds=self._parse_time(v)) for k, v in self.custom_breaks.items()}
            except (ValueError, TypeError):
                raise ValidationError(
                    "Nieprawidłowy format w custom_breaks. Użyj formatu: {1: '00:15:00', 2: '00:10:00'}.")

    def _parse_time(self, time_str):
        h, m, s = map(int, time_str.split(':'))
        return h * 3600 + m * 60 + s

    def __str__(self):
        return f"Konfiguracja czasu dla {self.institution.name}"

