from django.contrib import admin
from .models import Department

class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'faculty')

admin.site.register(Department, DepartmentAdmin)

