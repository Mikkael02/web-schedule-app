from django.urls import path
from . import views

app_name = 'room_types'

urlpatterns = [
    path('', views.manage_room_types, name='manage_room_types'),
    path('edit/<int:pk>/', views.edit_room_type, name='edit_room_type'),
    path('delete/<int:pk>/', views.delete_room_type, name='delete_room_type'),
]
