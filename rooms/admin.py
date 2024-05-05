from django.contrib import admin
from .models import Room, RoomType, Equipment


class RoomAdmin(admin.ModelAdmin):
    list_display = ('name', 'capacity', 'list_room_types', 'list_equipment')

    def list_room_types(self, obj):
        return ", ".join([room_type.type for room_type in obj.room_types.all()])

    list_room_types.short_description = 'Room Types'

    def list_equipment(self, obj):
        return ", ".join([equipment.name for equipment in obj.equipment.all()])

    list_equipment.short_description = 'Equipment'


admin.site.register(Room, RoomAdmin)
admin.site.register(RoomType)
admin.site.register(Equipment)
