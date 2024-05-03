from django.contrib import admin
from .models import Teacher

class TeacherAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email')
    search_fields = ('first_name', 'last_name', 'email')
    # Po dodaniu modelu Specialization można dodać list_filter = ('specializations',)

admin.site.register(Teacher, TeacherAdmin)
