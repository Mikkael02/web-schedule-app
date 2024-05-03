from django.urls import path
from .views import teacher_list, teacher_create, teacher_detail

urlpatterns = [
    path('', teacher_list, name='teacher_list'),
    path('create/', teacher_create, name='teacher_create'),
    path('<int:pk>/', teacher_detail, name='teacher_detail'),
]
