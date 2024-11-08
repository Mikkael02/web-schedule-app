# institutions/views.py
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Institution
from rooms.models import Room
from teachers.models import Teacher
from course.models import Course
from group.models import Group
from department.models import Department
from faculty.models import Faculty
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from .forms import GroupForm, TeacherForm, CourseForm  # Dodamy formularze
from rooms.models import Room, RoomType, Equipment
from course.models import Course
from .forms import RoomForm, CourseForm

def higher_education_view(request, institution_id):
    institution = get_object_or_404(Institution, pk=institution_id)
    faculties = institution.faculties.all()  # Pobieranie powiązanych wydziałów
    rooms = Room.objects.filter(institution=institution)  # Pobieranie powiązanych sal
    teachers = Teacher.objects.filter(institution=institution)  # Pobieranie powiązanych nauczycieli
    courses = Course.objects.filter(institution=institution)  # Pobieranie powiązanych kursów
    groups = Group.objects.filter(institution=institution)  # Pobieranie powiązanych grup
    context = {
        'institution': institution,
        'faculties': faculties,
        'rooms': rooms,
        'teachers': teachers,
        'courses': courses,
        'groups': groups
    }
    return render(request, 'higher_template.html', context)

def faculty_departments(request, faculty_id):
    departments = Department.objects.filter(faculty_id=faculty_id).values('name').distinct()
    departments_data = [{'name': department['name']} for department in departments]
    return JsonResponse(departments_data, safe=False)

def department_semesters(request, faculty_id, department_name):
    groups = Group.objects.filter(department__faculty_id=faculty_id, department__name=department_name).values('level').distinct()
    semesters = [{'number': group['level']} for group in groups]
    return JsonResponse(semesters, safe=False)

def semester_groups(request, faculty_id, department_name, level):
    groups = Group.objects.filter(department__faculty_id=faculty_id, department__name=department_name, level=level)
    groups_data = [{'id': group.id, 'name': group.name} for group in groups]
    return JsonResponse(groups_data, safe=False)

def institution_detail(request, institution_id):
    institution = Institution.objects.get(id=institution_id)
    rooms = Room.objects.filter(institution=institution)
    teachers = Teacher.objects.filter(institution=institution)
    faculties = Faculty.objects.filter(institution=institution)

    hours = ["8:00", "9:00", "10:00", "11:00", "12:00", "13:00", "14:00", "15:00", "16:00", "17:00", "18:00", "19:00",
             "20:00", "21:00", "22:00"]

    context = {
        'institution': institution,
        'rooms': rooms,
        'teachers': teachers,
        'faculties': faculties,
        'hours': hours
    }
    return render(request, 'higher_template.html', context)


def view_plan(request, plan_id):
    plan = get_object_or_404(Institution, id=plan_id)

    # Wybierz odpowiedni szablon na podstawie typu instytucji
    if plan.type == 'primary':
        template_name = 'primary_template.html'
    elif plan.type == 'secondary':
        template_name = 'secondary_template.html'
    elif plan.type == 'higher':
        template_name = 'higher_template.html'
    else:
        template_name = 'default_template.html'

    faculties = Faculty.objects.filter(institution=plan)
    rooms = Room.objects.filter(institution=plan)
    teachers = Teacher.objects.filter(institution=plan)

    context = {
        'institution': plan,
        'faculties': faculties,
        'rooms': rooms,
        'teachers': teachers,
    }

    return render(request, template_name, context)

@login_required
def delete_plan(request, plan_id):
    plan = get_object_or_404(Institution, id=plan_id, owner=request.user)
    plan.delete()
    return redirect('plans')

# Zarządzanie salami

def manage_rooms(request, institution_id):
    institution = get_object_or_404(Institution, id=institution_id)
    rooms = Room.objects.filter(institution=institution)
    room_types = RoomType.objects.filter(owner=request.user)
    equipment = Equipment.objects.filter(owner=request.user)

    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            room = form.save(commit=False)
            room.institution = institution
            room.save()
            room.room_types.set(request.POST.getlist('room_types'))
            room.equipment.set(request.POST.getlist('equipment'))
            return redirect('manage_rooms', institution_id=institution.id)
    else:
        form = RoomForm()

    return render(request, 'accounts/primary/primary_manage_rooms.html', {
        'institution': institution,
        'rooms': rooms,
        'room_types': room_types,
        'equipment': equipment,
        'form': form
    })

# Zarządzanie klasami
def manage_groups(request, institution_id):
    institution = get_object_or_404(Institution, id=institution_id)
    groups = Group.objects.filter(institution=institution)

    if request.method == 'POST':
        form = GroupForm(request.POST)
        if form.is_valid():
            group = form.save(commit=False)
            group.institution = institution
            group.save()
            return redirect('manage_groups', institution_id=institution.id)
    else:
        form = GroupForm()

    return render(request, 'accounts/primary/primary_manage_groups.html', {
        'institution': institution,
        'groups': groups,
        'form': form,
    })

# Zarządzanie nauczycielami
def manage_teachers(request, institution_id):
    institution = get_object_or_404(Institution, id=institution_id)
    teachers = Teacher.objects.filter(institution=institution)

    if request.method == 'POST':
        form = TeacherForm(request.POST)
        if form.is_valid():
            teacher = form.save(commit=False)
            teacher.institution = institution
            teacher.save()
            return redirect('manage_teachers', institution_id=institution.id)
    else:
        form = TeacherForm()

    return render(request, 'accounts/primary/primary_manage_teachers.html', {
        'institution': institution,
        'teachers': teachers,
        'form': form,
    })

# Zarządzanie zajęciami

def manage_courses(request, institution_id):
    institution = get_object_or_404(Institution, id=institution_id)
    courses = Course.objects.filter(institution=institution)
    room_types = RoomType.objects.filter(owner=request.user)
    equipment = Equipment.objects.filter(owner=request.user)

    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            course = form.save(commit=False)
            course.institution = institution
            course.save()
            course.room_types.set(request.POST.getlist('course_types'))
            course.equipment.set(request.POST.getlist('equipment'))
            return redirect('manage_courses', institution_id=institution.id)
    else:
        form = CourseForm()

    return render(request, 'accounts/primary/primary_manage_courses.html', {
        'institution': institution,
        'courses': courses,
        'room_types': room_types,
        'equipment': equipment,
        'form': form
    })
