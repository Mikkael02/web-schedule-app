from django.urls import path
from .views import room_list, room_create, room_detail

urlpatterns = [
    path('', room_list, name='room_list'),
    path('create/', room_create, name='room_create'),
    path('<int:pk>/', room_detail, name='room_detail'),
]
