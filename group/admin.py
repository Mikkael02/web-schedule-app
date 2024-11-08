from django.contrib import admin
from .models import Group

class GroupAdmin(admin.ModelAdmin):
    list_display = ['name', 'department', 'size', 'level', 'institution']
    list_filter = ['department', 'level']
    search_fields = ['name', 'department']

admin.site.register(Group, GroupAdmin)