from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from group.models import Group
from rooms.models import Room
from teachers.models import Teacher
from django.shortcuts import render, get_object_or_404, redirect
from .models import Institution, Course, Group, Schedule
from department.models import Department
from TimeConfiguration.forms import TimeConfigurationForm
from TimeConfiguration.models import TimeConfiguration
from SubjectFrequency.models import SubjectFrequency
from datetime import timedelta, datetime
import json
from schedules.forms import ManualScheduleForm
from django.http import JsonResponse
from time import sleep


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
            schedule.end_time = (
                datetime.combine(datetime.today(), schedule.start_time) +
                time_config.lesson_duration
            ).time()

            selected_groups = form.cleaned_data['group']

            # Walidacja konfliktów i wymagań sali oraz nauczyciela
            if check_conflicts(schedule, schedules):
                form.add_error(None, "Konflikt z istniejącymi zajęciami.")
            elif not check_room_requirements(schedule.course, schedule.room):
                form.add_error(None, "Sala nie spełnia wymagań zajęć.")
            elif not check_teacher_courses(schedule.teacher, schedule.course):
                form.add_error(None, "Nauczyciel nie może prowadzić wybranych zajęć.")
            elif not check_room_capacity(selected_groups, schedule.room):
                form.add_error(None, "Sala nie może pomieścić wszystkich uczniów.")
            else:
                schedule.institution = institution
                schedule.save()
                schedule.group.set(selected_groups)  # Przypisz grupy
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
    """Sprawdź czy nowy harmonogram koliduje z istniejącymi zajęciami, uwzględniając typ tygodnia."""
    for schedule in existing_schedules:
        # Sprawdzenie konfliktu na poziomie sali lub nauczyciela
        if (
            (schedule.room == new_schedule.room or
             schedule.teacher == new_schedule.teacher) and
            schedule.day_of_week == new_schedule.day_of_week and
            not (new_schedule.start_time >= schedule.end_time or new_schedule.end_time <= schedule.start_time)
        ):
            # Sprawdzenie konfliktu typów tygodnia
            if (
                schedule.week_type == 'weekly' or
                new_schedule.week_type == 'weekly' or
                schedule.week_type == new_schedule.week_type
            ):
                return True
    return False

def check_teacher_courses(teacher, course):
    """Sprawdź czy nauczyciel może prowadzić dane zajęcia."""
    return course in teacher.courses.all()

def check_room_capacity(group, room):
    """Sprawdź czy sala ma wystarczającą pojemność dla grupy."""
    return group.size <= room.capacity

def check_room_requirements(course, room):
    """Sprawdź czy sala spełnia wymagania zajęć."""
    required_types = course.room_types.all()
    required_equipment = course.equipment.all()

    return (
            all(rt in room.room_types.all() for rt in required_types) and
            all(eq in room.equipment.all() for eq in required_equipment)
    )

@login_required
def automatic_schedule(request, institution_id):
    institution = get_object_or_404(Institution, id=institution_id)
    schedules = Schedule.objects.filter(institution=institution)
    frequencies = SubjectFrequency.objects.filter(institution=institution)
    time_config = get_object_or_404(TimeConfiguration, institution=institution)

    days_mapping = {
        'full': ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'],
        'normal': ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'],
        'weekend': ['Saturday', 'Sunday']
    }

    if request.method == 'POST':
        selected_days = request.POST.get('days', 'normal')
        days = days_mapping[selected_days]

        schedules.delete()

        start_times = calculate_start_times(time_config)
        existing_schedules = []
        errors = []
        total_tasks = frequencies.count()
        completed_tasks = 0

        for freq in frequencies:
            main_group = freq.group  # Główna grupa
            course = freq.course
            teacher = course.teacher_set.first()  # Pobieramy nauczyciela przypisanego do kursu
            room = find_suitable_room(course, institution, main_group)

            if not room:
                errors.append(f"Brak dostępnych sal dla kursu {course.name} w grupie {main_group.name}.")
                continue
            if not teacher or not check_teacher_courses(teacher, course):
                errors.append(f"Brak nauczyciela dla kursu {course.name}.")
                continue

            # Pobieramy grupy współdzielące zajęcia
            shared_groups = list(freq.shared_groups.all())
            if shared_groups:
                # Tworzymy jedno zajęcia dla grup wspólnych
                participating_groups = shared_groups + [main_group]
                weekly_sessions = int(freq.frequency)
                biweekly_sessions = 1 if freq.frequency % 1 > 0 else 0
                week_types = ['weekly'] * weekly_sessions
                if biweekly_sessions:
                    week_types.append('odd' if len(week_types) % 2 == 0 else 'even')

                for week_type in week_types:
                    placed = False
                    for day in days:
                        for start_time in start_times:
                            end_time = (datetime.combine(datetime.today(), start_time) + time_config.lesson_duration).time()
                            potential_schedule = Schedule(
                                institution=institution,
                                course=course,
                                teacher=teacher,
                                room=room,
                                week_type=week_type,
                                day_of_week=day,
                                start_time=start_time,
                                end_time=end_time,
                            )
                            if not check_conflicts_for_shared(potential_schedule, participating_groups, existing_schedules):
                                schedule = Schedule.objects.create(
                                    institution=institution,
                                    course=course,
                                    teacher=teacher,
                                    room=room,
                                    week_type=week_type,
                                    day_of_week=day,
                                    start_time=start_time,
                                    end_time=end_time,
                                )
                                schedule.group.set(participating_groups)
                                existing_schedules.append(schedule)
                                placed = True
                                break
                        if placed:
                            break
                    if not placed:
                        errors.append(f"Nie udało się umieścić kursu {course.name} dla grupy wspólnej: {', '.join([g.name for g in participating_groups])}.")
            else:
                # Tworzymy zajęcia osobno dla każdej grupy na tym samym poziomie
                all_groups = Group.objects.filter(level=main_group.level, institution=institution)
                for individual_group in all_groups:
                    weekly_sessions = int(freq.frequency)
                    biweekly_sessions = 1 if freq.frequency % 1 > 0 else 0
                    week_types = ['weekly'] * weekly_sessions
                    if biweekly_sessions:
                        week_types.append('odd' if len(week_types) % 2 == 0 else 'even')

                    for week_type in week_types:
                        placed = False
                        for day in days:
                            for start_time in start_times:
                                end_time = (datetime.combine(datetime.today(), start_time) + time_config.lesson_duration).time()
                                potential_schedule = Schedule(
                                    institution=institution,
                                    course=course,
                                    teacher=teacher,
                                    room=room,
                                    week_type=week_type,
                                    day_of_week=day,
                                    start_time=start_time,
                                    end_time=end_time,
                                )
                                if not check_conflicts_for_shared(potential_schedule, [individual_group], existing_schedules):
                                    schedule = Schedule.objects.create(
                                        institution=institution,
                                        course=course,
                                        teacher=teacher,
                                        room=room,
                                        week_type=week_type,
                                        day_of_week=day,
                                        start_time=start_time,
                                        end_time=end_time,
                                    )
                                    schedule.group.set([individual_group])
                                    existing_schedules.append(schedule)
                                    placed = True
                                    break
                            if placed:
                                break
                        if not placed:
                            errors.append(f"Nie udało się umieścić kursu {course.name} w grupie {individual_group.name}.")

            completed_tasks += 1

        return JsonResponse({
            'completed_tasks': completed_tasks,
            'total_tasks': total_tasks,
            'errors': errors,
        })

    return render(request, 'schedules/automatic_schedule.html', {
        'institution': institution,
        'days_mapping': days_mapping,
    })


def find_suitable_room(course, institution, group):
    """Znajdź odpowiednią salę z uwzględnieniem wymagań kursu i pojemności."""
    rooms = Room.objects.filter(institution=institution)
    for room in rooms:
        if check_room_requirements(course, room) and check_room_capacity(group, room):
            return room
    return None


def check_conflicts_for_shared(new_schedule, groups, existing_schedules):
    """Sprawdź konflikty dla zajęć współdzielonych."""
    for schedule in existing_schedules:
        if schedule.day_of_week == new_schedule.day_of_week and (
                (any(group in schedule.group.all() for group in groups) or
                 schedule.teacher == new_schedule.teacher or
                 schedule.room == new_schedule.room) and
                new_schedule.start_time < schedule.end_time and new_schedule.end_time > schedule.start_time
        ):
            if (
                    schedule.week_type == 'weekly' or
                    new_schedule.week_type == 'weekly' or
                    schedule.week_type == new_schedule.week_type
            ):
                return True
    return False
