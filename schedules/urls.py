from django.urls import path
from .views import schedule_list, schedule_detail, schedule_create

urlpatterns = [
    path('', schedule_list, name='schedule_list'),
    path('create/', schedule_create, name='schedule_create'),
    path('<int:pk>/', schedule_detail, name='schedule_detail'),
]
