from django.contrib import admin
from .models import Institution

class InstitutionAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'location')
    list_filter = ('type', 'location')
    search_fields = ('name', 'location')

admin.site.register(Institution, InstitutionAdmin)
