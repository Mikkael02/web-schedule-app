from django.urls import path
from . import views

app_name = 'room_types'

urlpatterns = [
    path('manage-room-types/rooms/', views.manage_room_types_rooms, name='manage_room_types_rooms'),
    path('manage-room-types/courses/', views.manage_room_types_courses, name='manage_room_types_courses'),
    path('edit/<str:context>/<int:pk>/', views.edit_room_type, name='edit_room_type'),
    path('delete/<str:context>/<int:pk>/', views.delete_room_type, name='delete_room_type'),
]
