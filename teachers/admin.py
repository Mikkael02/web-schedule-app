from django.contrib import admin
from .models import Teacher

class TeacherAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'title')
    search_fields = ('first_name', 'last_name', 'email', 'title')
    # Po dodaniu modelu Specialization można dodać list_filter = ('specializations',)

admin.site.register(Teacher, TeacherAdmin)
