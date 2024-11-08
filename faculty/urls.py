# faculties/urls.py
from django.urls import path
from .views import FacultyListView
from .views import FacultyDetailView

urlpatterns = [
    path('faculties/', FacultyListView.as_view(), name='faculties-list'),
    path('faculties/<int:pk>/', FacultyDetailView.as_view(), name='faculties-detail'),
]
