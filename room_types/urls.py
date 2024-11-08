from django.urls import path
from .views import add_room_type

urlpatterns = [
    path('add/', add_room_type, name='add_room_type'),
]
