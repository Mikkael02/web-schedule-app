from django.urls import path
from .views import CourseListView, CourseCreateView, CourseUpdateView, CourseDeleteView

urlpatterns = [
    path('', CourseListView.as_view(), name='course_list'),
    path('create/', CourseCreateView.as_view(), name='course_create'),
    path('update/<int:pk>/', CourseUpdateView.as_view(), name='course_update'),
    path('delete/<int:pk>/', CourseDeleteView.as_view(), name='course_delete'),
]
