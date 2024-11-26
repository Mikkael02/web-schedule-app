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
from schedules.views import generate_schedule
from TimeConfiguration.views import configure_time
from schedules.views import manual_schedule, automatic_schedule
from SubjectFrequency.views import define_subject_frequency

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
    #path('<int:institution_id>/rooms/edit/<int:room_id>/', views.edit_room, name='edit_room'),
    path('<int:institution_id>/rooms/edit/<int:pk>/', views.edit_room, name='edit_room'),
    path('<int:institution_id>/rooms/delete/<int:room_id>/', views.delete_room, name='delete_room'),
    path('<int:institution_id>/groups/', views.manage_groups, name='manage_groups'),
    path('<int:institution_id>/groups/edit/<int:group_id>/', views.edit_group, name='edit_group'),
    path('<int:institution_id>/groups/delete/<int:group_id>/', views.delete_group, name='delete_group'),
    path('<int:institution_id>/teachers/', views.manage_teachers, name='manage_teachers'),
    path('<int:institution_id>/teachers/edit/<int:teacher_id>/', views.edit_teacher, name='edit_teacher'),
    path('<int:institution_id>/teachers/delete/<int:teacher_id>/', views.delete_teacher, name='delete_teacher'),
    path('<int:institution_id>/courses/', views.manage_courses, name='manage_courses'),
    path('<int:institution_id>/courses/edit/<int:course_id>/', views.edit_course, name='edit_course'),
    path('<int:institution_id>/courses/delete/<int:course_id>/', views.delete_course, name='delete_course'),
    path('<int:institution_id>/departments/', views.manage_departments, name='manage_departments'),
    path('<int:institution_id>/departments/edit/<int:department_id>/', views.edit_department, name='edit_department'),
    path('<int:institution_id>/departments/delete/<int:department_id>/', views.delete_department, name='delete_department'),
    path('<int:institution_id>/faculties/', views.manage_faculties, name='manage_faculties'),
    path('<int:institution_id>/faculties/edit/<int:faculty_id>/', views.edit_faculty, name='edit_faculty'),
    path('<int:institution_id>/faculties/delete/<int:faculty_id>/', views.delete_faculty, name='delete_faculty'),
    path('<int:institution_id>/generate-schedule/', generate_schedule, name='generate_schedule'),
    path('<int:institution_id>/configure-time/', configure_time, name='configure_time'),
    path('<int:institution_id>/manual-schedule/', manual_schedule, name='manual_schedule'),
    path('<int:institution_id>/define-subject-frequency/', define_subject_frequency,
         name='define_subject_frequency'),
    path('<int:institution_id>/automatic-schedule/', automatic_schedule, name='automatic_schedule'),



    # Add additional API endpoints for plans
    path('plans/api/faculties/<int:faculty_id>/departments/', faculty_departments, name='plan-faculty-departments'),
    path('plans/api/faculties/<int:faculty_id>/departments/<str:department_name>/semesters/', department_semesters,
         name='plan-department-semesters'),
    path('plans/api/faculties/<int:faculty_id>/departments/<str:department_name>/semesters/<str:level>/groups/',
         semester_groups, name='plan-semester-groups'),
]
