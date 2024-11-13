from django.urls import path
from . import views

app_name = 'equipment'

urlpatterns = [
    path('manage-equipment/rooms/', views.manage_equipment_rooms, name='manage_equipment_rooms'),
    path('manage-equipment/courses/', views.manage_equipment_courses, name='manage_equipment_courses'),
    path('edit/<str:context>/<int:pk>/', views.edit_equipment, name='edit_equipment'),
    path('delete/<str:context>/<int:pk>/', views.delete_equipment, name='delete_equipment'),
]
