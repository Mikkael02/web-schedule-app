from django.urls import path
from . import views

app_name = 'equipment'

urlpatterns = [
    path('', views.manage_equipment, name='manage_equipment'),
    path('edit/<int:pk>/', views.edit_equipment, name='edit_equipment'),
    path('delete/<int:pk>/', views.delete_equipment, name='delete_equipment'),
]
