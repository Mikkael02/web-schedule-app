from django.contrib import admin
from .models import Room

class RoomAdmin(admin.ModelAdmin):
    list_display = ('name', 'capacity', 'room_type')
    list_filter = ('room_type',)
    search_fields = ('name',)

admin.site.register(Room, RoomAdmin)
