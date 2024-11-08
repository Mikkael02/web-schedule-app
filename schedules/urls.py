from django.urls import path
from .views import schedule_list, schedule_detail, schedule_create
from .views import get_schedule_for_group, get_schedule_for_room, get_schedule_for_teacher

urlpatterns = [
    path('', schedule_list, name='schedule_list'),
    path('create/', schedule_create, name='schedule_create'),
    path('<int:pk>/', schedule_detail, name='schedule_detail'),
    path('groups/<int:group_id>/schedule/', get_schedule_for_group, name='schedule_for_group'),
    path('rooms/<int:room_id>/schedule/', get_schedule_for_room, name='schedule_for_room'),
    path('teachers/<int:teacher_id>/schedule/', get_schedule_for_teacher, name='schedule_for_teacher'),
]
