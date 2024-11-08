from django.urls import path
from .views import (
    higher_education_view,
    faculty_departments,
    department_semesters,
    semester_groups,
    view_plan,
    delete_plan
)
from . import views

urlpatterns = [
    path('higher-education/<int:institution_id>/', higher_education_view, name='higher-education'),

    # API routes for institution
    path('api/faculties/<int:faculty_id>/departments/', faculty_departments, name='faculty-departments'),
    path('api/faculties/<int:faculty_id>/departments/<str:department_name>/semesters/', department_semesters,
         name='department-semesters'),
    path('api/faculties/<int:faculty_id>/departments/<str:department_name>/semesters/<str:level>/groups/',
         semester_groups, name='semester-groups'),

    # View a plan (using same API logic)
    path('plans/<int:plan_id>/', view_plan, name='view_plan'),
    path('delete-plan/<int:plan_id>/', delete_plan, name='delete_plan'),
    path('<int:institution_id>/rooms/', views.manage_rooms, name='manage_rooms'),
    path('<int:institution_id>/groups/', views.manage_groups, name='manage_groups'),
    path('<int:institution_id>/teachers/', views.manage_teachers, name='manage_teachers'),
    path('<int:institution_id>/courses/', views.manage_courses, name='manage_courses'),


    # Add additional API endpoints for plans
    path('plans/api/faculties/<int:faculty_id>/departments/', faculty_departments, name='plan-faculty-departments'),
    path('plans/api/faculties/<int:faculty_id>/departments/<str:department_name>/semesters/', department_semesters,
         name='plan-department-semesters'),
    path('plans/api/faculties/<int:faculty_id>/departments/<str:department_name>/semesters/<str:level>/groups/',
         semester_groups, name='plan-semester-groups'),
]
