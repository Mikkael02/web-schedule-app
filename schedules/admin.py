from django.contrib import admin
from .models import Schedule

class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('course', 'group', 'room', 'teacher', 'day_of_week', 'start_time', 'end_time')
    list_filter = ('day_of_week', 'course', 'room', 'teacher', 'group')
    search_fields = ('course__name', 'group__name', 'room__name', 'teacher__first_name', 'teacher__last_name')

admin.site.register(Schedule, ScheduleAdmin)