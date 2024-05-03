from django.contrib import admin
from .models import Schedule
from .models import Room, Teacher  # Upewnij się, że importujesz potrzebne modele

class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('course', 'room', 'teacher', 'time_slot')
    list_filter = ('room', 'teacher')
    search_fields = ('course',)
    autocomplete_fields = ['room', 'teacher']  # Ułatwia wybór dla ForeignKey

admin.site.register(Schedule, ScheduleAdmin)
