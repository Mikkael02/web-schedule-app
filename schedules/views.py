from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from .forms import ScheduleForm
from django.http import JsonResponse
from group.models import Group
from rooms.models import Room
from teachers.models import Teacher
from django.shortcuts import render, get_object_or_404, redirect
from .models import Institution, Course, Group, Schedule
from .forms import CourseAssignmentForm
from department.models import Department
from TimeConfiguration.forms import TimeConfigurationForm
from TimeConfiguration.models import TimeConfiguration
from datetime import timedelta
import json

def schedule_list(request):
    schedules = Schedule.objects.all()  # Pobiera wszystkie obiekty Schedule z bazy danych
    return render(request, 'schedules/schedule_list.html', {'schedules': schedules})

def schedule_create(request):
    if request.method == 'POST':
        form = ScheduleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('schedule_list')
    else:
        form = ScheduleForm()
    return render(request, 'schedules/schedule_form.html', {'form': form})

def schedule_detail(request, pk):
    schedule = Schedule.objects.get(pk=pk)
    return render(request, 'schedules/schedule_detail.html', {'schedule': schedule})

def get_schedule_data(schedules):
    week_type_display = {
        'weekly': 'Co tydzień',
        'even': 'Tygodnie parzyste',
        'odd': 'Tygodnie nieparzyste'
    }

    course_type_display = {
        'lecture': 'Wykład',
        'lab': 'Lab',
        'seminar': 'Seminarium',
        'project': 'PRO',
        'exercises': 'ĆW',
        'sport': 'Ćwiczenia sportowe'
    }

    schedule_data = [
        {
            'course_type': course_type_display.get(schedule.course.course_type, schedule.course.course_type),
            'week_type': week_type_display[schedule.week_type],
            'room': schedule.room.name,
            'room_id': schedule.room.id,
            'course': schedule.course.name,
            'teacher': f"{schedule.teacher.title} {schedule.teacher.first_name} {schedule.teacher.last_name}",
            'teacher_id': schedule.teacher.id,
            'group': f"{schedule.group.department.name} [{schedule.group.name}]" if schedule.group.department else schedule.group.name,
            'group_id': schedule.group.id,
            'day_of_week': schedule.day_of_week,
            'start_time': schedule.start_time.strftime('%H:%M'),
            'end_time': schedule.end_time.strftime('%H:%M')
        } for schedule in schedules
    ]
    return schedule_data


def get_schedule_for_group(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    schedules = Schedule.objects.filter(group=group)
    schedule_data = get_schedule_data(schedules)
    return JsonResponse(schedule_data, safe=False)


def get_schedule_for_room(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    schedules = Schedule.objects.filter(room=room)
    schedule_data = get_schedule_data(schedules)
    return JsonResponse(schedule_data, safe=False)


def get_schedule_for_teacher(request, teacher_id):
    teacher = get_object_or_404(Teacher, id=teacher_id)
    schedules = Schedule.objects.filter(teacher=teacher)
    schedule_data = get_schedule_data(schedules)
    return JsonResponse(schedule_data, safe=False)

@login_required
def generate_schedule(request, institution_id):
    institution = get_object_or_404(Institution, id=institution_id)

    time_config, created = TimeConfiguration.objects.get_or_create(
        institution=institution,
        defaults={
            'start_time': '08:00',
            'end_time': '20:00',
            'lesson_duration': timedelta(minutes=90),
            'break_type': 'same',
            'break_duration': timedelta(minutes=30),
            'custom_breaks': json.dumps({})
        }
    )

    if request.method == 'POST':
        form = TimeConfigurationForm(request.POST, instance=time_config)
        if form.is_valid():
            time_config = form.save(commit=False)
            if time_config.break_type == 'custom':
                time_config.custom_breaks = form.cleaned_data['custom_breaks']
            else:
                time_config.custom_breaks = json.dumps({})
            time_config.save()
            return redirect('generate_schedule', institution_id=institution.id)
    else:
        form = TimeConfigurationForm(instance=time_config)

    return render(request, 'schedules/generate_schedule.html', {
        'institution': institution,
        'time_config': time_config,
        'form': form,
    })
