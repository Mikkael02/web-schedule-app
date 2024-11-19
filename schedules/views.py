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
from department.models import Department
from TimeConfiguration.forms import TimeConfigurationForm
from TimeConfiguration.models import TimeConfiguration
from datetime import timedelta, datetime
import json
from schedules.forms import ManualScheduleForm
from django.db.models import Q

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

@login_required
def manual_schedule(request, institution_id):
    institution = get_object_or_404(Institution, id=institution_id)
    time_config = get_object_or_404(TimeConfiguration, institution=institution)
    schedules = Schedule.objects.filter(institution=institution)

    # Oblicz dostępne opcje dla start_time
    start_times = calculate_start_times(time_config)

    if request.method == 'POST':
        form = ManualScheduleForm(request.POST, institution=institution, start_times=start_times)
        if form.is_valid():
            schedule = form.save(commit=False)
            # Automatyczne ustawienie end_time
            schedule.end_time = (
                    datetime.combine(datetime.today(), schedule.start_time) +
                    time_config.lesson_duration
            ).time()

            # Walidacja konfliktów i wymagań sali
            if check_conflicts(schedule, schedules):
                form.add_error(None, "Konflikt z istniejącymi zajęciami.")
            elif not check_room_requirements(schedule.course, schedule.room):
                form.add_error(None, "Sala nie spełnia wymagań zajęć.")
            else:
                schedule.institution = institution
                schedule.save()
                return redirect('manual_schedule', institution_id=institution.id)
    else:
        form = ManualScheduleForm(institution=institution, start_times=start_times)

    return render(request, 'schedules/manual_schedule.html', {
        'institution': institution,
        'form': form,
        'schedules': schedules,
    })

def calculate_start_times(time_config):
    """Generuje dostępne godziny rozpoczęcia zajęć w oparciu o konfigurację czasu."""
    times = []
    current_time = time_config.start_time

    if time_config.break_type == 'same':
        # Przerwy o tej samej długości
        while current_time < time_config.end_time:
            times.append(current_time)
            next_time = (
                datetime.combine(datetime.today(), current_time) +
                time_config.lesson_duration +
                (time_config.break_duration if time_config.break_duration else timedelta())
            )
            current_time = next_time.time()
    elif time_config.break_type == 'custom':
        # Przerwy o różnej długości: dodajemy pierwszą godzinę startu + czasy zgodnie z konfiguracją przerw
        times.append(current_time)  # Dodajemy start pierwszych zajęć
        for i in range(1, len(time_config.custom_breaks) + 1):
            custom_break = time_config.custom_breaks.get(str(i), '00:00:00')
            h, m, s = map(int, custom_break.split(':'))
            next_time = (
                datetime.combine(datetime.today(), current_time) +
                time_config.lesson_duration +
                timedelta(hours=h, minutes=m, seconds=s)
            )
            current_time = next_time.time()
            if current_time < time_config.end_time:
                times.append(current_time)
            else:
                break

    return times

def check_conflicts(new_schedule, existing_schedules):
    """Sprawdź czy nowy harmonogram koliduje z istniejącymi zajęciami."""
    for schedule in existing_schedules:
        if (
                (schedule.group == new_schedule.group or
                 schedule.room == new_schedule.room or
                 schedule.teacher == new_schedule.teacher) and
                schedule.day_of_week == new_schedule.day_of_week and
                not (new_schedule.start_time >= schedule.end_time or new_schedule.end_time <= schedule.start_time)
        ):
            return True
    return False


def check_room_requirements(course, room):
    """Sprawdź czy sala spełnia wymagania zajęć."""
    required_types = course.room_types.all()
    required_equipment = course.equipment.all()

    return (
            all(rt in room.room_types.all() for rt in required_types) and
            all(eq in room.equipment.all() for eq in required_equipment)
    )
