from django.contrib import admin
from .models import Teacher


class TeacherAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'title', 'display_courses', 'institution')

    def display_courses(self, obj):
        return ", ".join([course.name for course in obj.courses.all()])

    display_courses.short_description = 'Kursy'


admin.site.register(Teacher, TeacherAdmin)
