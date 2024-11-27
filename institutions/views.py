# institutions/views.py
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Institution
from rooms.models import Room
from teachers.models import Teacher
from group.models import Group
from department.models import Department
from faculty.models import Faculty
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from .forms import GroupForm, TeacherForm
from rooms.models import Room, RoomType, Equipment
from course.models import Course
from .forms import RoomForm, CourseForm, DepartmentForm, FacultyForm
import os
from django.conf import settings

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

    # Usuń logo, jeśli istnieje
    if plan.logo:
        logo_path = os.path.join(settings.MEDIA_ROOT, plan.logo.name)
        if os.path.isfile(logo_path):
            os.remove(logo_path)

    # Usuń obiekt planu
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

    if institution.type == 'primary':
        template = 'accounts/primary/primary_manage_rooms.html'
    elif institution.type == 'secondary':
        template = 'accounts/secondary/secondary_manage_rooms.html'
    else:
        template = 'accounts/higher/higher_manage_rooms.html'

    return render(request, template, {
        'institution': institution,
        'rooms': rooms,
        'room_types': room_types,
        'equipment': equipment,
        'form': form
    })

@login_required
def edit_room(request, institution_id, pk):
    room = get_object_or_404(Room, pk=pk, institution_id=institution_id)
    room_types = RoomType.objects.filter(owner=request.user)
    equipment = Equipment.objects.filter(owner=request.user)

    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            room = form.save()
            room.room_types.set(form.cleaned_data['room_types'])
            room.equipment.set(form.cleaned_data['equipment'])
            room.save()
            return redirect('manage_rooms', institution_id=institution_id)
    else:
        form = RoomForm(instance=room)

    context = {
        'form': form,
        'room': room,
        'room_types': room_types,
        'equipment': equipment,
    }
    return render(request, 'rooms/edit_room.html', context)

@login_required
def delete_room(request, institution_id, room_id):
    room = get_object_or_404(Room, id=room_id, institution_id=institution_id)
    room.delete()
    return redirect('manage_rooms', institution_id=institution_id)

@login_required
def manage_groups(request, institution_id):
    institution = get_object_or_404(Institution, id=institution_id)
    groups = Group.objects.filter(institution=institution)

    # Filtrowanie department na podstawie typu instytucji
    if institution.type == 'secondary':
        # W secondary korzystamy z nowego pola `institution`
        departments = Department.objects.filter(institution=institution)
    elif institution.type == 'higher':
        # W higher korzystamy z `faculty`
        departments = Department.objects.filter(faculty__institution=institution)
    else:  # primary
        departments = []

    # Ograniczenia dla level_choices w zależności od typu instytucji
    if institution.type == 'primary':
        level_choices = [(choice, display) for choice, display in Group.LEVEL_CHOICES if choice.isdigit() and 1 <= int(choice) <= 8]
        template = 'accounts/primary/primary_manage_groups.html'
    elif institution.type == 'secondary':
        level_choices = [(choice, display) for choice, display in Group.LEVEL_CHOICES if choice.isdigit() and 1 <= int(choice) <= 5]
        template = 'accounts/secondary/secondary_manage_groups.html'
    else:  # higher
        level_choices = [(choice, display) for choice, display in Group.LEVEL_CHOICES if choice.startswith('S')]
        template = 'accounts/higher/higher_manage_groups.html'

    if request.method == 'POST':
        form = GroupForm(request.POST, institution_type=institution.type)
        if form.is_valid():
            group = form.save(commit=False)
            group.institution = institution
            if institution.type in ['secondary', 'higher']:
                group.department = get_object_or_404(Department, id=request.POST.get('department'))
            group.save()
            return redirect('manage_groups', institution_id=institution.id)
    else:
        form = GroupForm(institution_type=institution.type)

    return render(request, template, {
        'institution': institution,
        'groups': groups,
        'form': form,
        'level_choices': level_choices,
        'departments': departments,  # Przekazujemy tylko dla secondary i higher
    })

@login_required
def edit_group(request, institution_id, group_id):
    institution = get_object_or_404(Institution, id=institution_id)
    group = get_object_or_404(Group, id=group_id, institution=institution)

    # Filtrujemy odpowiednie poziomy dla danej instytucji
    if institution.type == 'primary':
        level_choices = [(choice, display) for choice, display in Group.LEVEL_CHOICES if choice.isdigit() and int(choice) <= 8]
        departments = []
    elif institution.type == 'secondary':
        level_choices = [(choice, display) for choice, display in Group.LEVEL_CHOICES if choice.isdigit() and int(choice) <= 5]
        departments = Department.objects.filter(institution=institution)
    else:  # higher
        level_choices = [(choice, display) for choice, display in Group.LEVEL_CHOICES if 'S' in choice]
        departments = Department.objects.filter(faculty__institution=institution)

    if request.method == 'POST':
        form = GroupForm(request.POST, instance=group, institution_type=institution.type)
        if form.is_valid():
            group = form.save(commit=False)
            if institution.type in ['secondary', 'higher']:
                group.department = get_object_or_404(Department, id=request.POST.get('department'))
            group.save()
            return redirect('manage_groups', institution_id=institution.id)
    else:
        form = GroupForm(instance=group, institution_type=institution.type)

    return render(request, 'groups/edit_group.html', {
        'form': form,
        'group': group,
        'institution': institution,
        'level_choices': level_choices,
        'departments': departments,  # Lista profilów dla secondary/higher
    })

@login_required
def delete_group(request, institution_id, group_id):
    group = get_object_or_404(Group, id=group_id, institution_id=institution_id)
    group.delete()
    return redirect('manage_groups', institution_id=institution_id)

@login_required
def manage_teachers(request, institution_id):
    institution = get_object_or_404(Institution, id=institution_id)
    teachers = Teacher.objects.filter(institution=institution)
    courses = Course.objects.filter(institution=institution)  # Pobieramy kursy instytucji

    if request.method == 'POST':
        form = TeacherForm(request.POST)
        if form.is_valid():
            teacher = form.save(commit=False)
            teacher.institution = institution
            teacher.save()
            form.save_m2m()  # Zapisanie relacji ManyToMany
            return redirect('manage_teachers', institution_id=institution.id)
    else:
        form = TeacherForm()

    # Dynamiczny wybór szablonu na podstawie typu instytucji
    if institution.type == 'primary':
        template = 'accounts/primary/primary_manage_teachers.html'
    elif institution.type == 'secondary':
        template = 'accounts/secondary/secondary_manage_teachers.html'
    else:
        template = 'accounts/higher/higher_manage_teachers.html'

    return render(request, template, {
        'institution': institution,
        'teachers': teachers,
        'courses': courses,
        'form': form,
        'titles': Teacher.TITLES,  # Lista tytułów
    })

@login_required
def edit_teacher(request, institution_id, teacher_id):
    institution = get_object_or_404(Institution, id=institution_id)
    teacher = get_object_or_404(Teacher, id=teacher_id, institution=institution)
    courses = Course.objects.filter(institution=institution)

    if request.method == 'POST':
        form = TeacherForm(request.POST, instance=teacher)
        if form.is_valid():
            form.save()
            return redirect('manage_teachers', institution_id=institution.id)
    else:
        form = TeacherForm(instance=teacher)

    return render(request, 'teachers/edit_teacher.html', {
        'institution': institution,
        'teacher': teacher,
        'courses': courses,
        'form': form
    })


@login_required
def delete_teacher(request, institution_id, teacher_id):
    teacher = get_object_or_404(Teacher, id=teacher_id, institution_id=institution_id)
    teacher.delete()
    return redirect('manage_teachers', institution_id=institution_id)
# Zarządzanie zajęciami

@login_required
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
            form.save_m2m()  # Zapisanie relacji ManyToMany
            return redirect('manage_courses', institution_id=institution.id)
    else:
        form = CourseForm()

    if institution.type == 'primary':
        template = 'accounts/primary/primary_manage_courses.html'
    elif institution.type == 'secondary':
        template = 'accounts/secondary/secondary_manage_courses.html'
    else:
        template = 'accounts/higher/higher_manage_courses.html'

    return render(request, template, {
        'institution': institution,
        'courses': courses,
        'form': form,
        'room_types': room_types,
        'equipment': equipment,
    })

@login_required
def edit_course(request, institution_id, course_id):
    course = get_object_or_404(Course, id=course_id, institution_id=institution_id)
    room_types = RoomType.objects.filter(owner=request.user)
    equipment = Equipment.objects.filter(owner=request.user)

    if request.method == 'POST':
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            form.save_m2m()  # Zapisz relacje ManyToMany
            return redirect('manage_courses', institution_id=institution_id)
    else:
        form = CourseForm(instance=course)

    context = {
        'course': course,
        'form': form,
        'room_types': room_types,
        'equipment': equipment,
    }
    return render(request, 'courses/edit_course.html', context)

@login_required
def delete_course(request, institution_id, course_id):
    course = get_object_or_404(Course, id=course_id, institution_id=institution_id)
    course.delete()
    return redirect('manage_courses', institution_id=institution_id)

@login_required
def manage_departments(request, institution_id):
    institution = get_object_or_404(Institution, id=institution_id)
    if institution.type == 'higher':
        departments = Department.objects.filter(faculty__institution=institution)
        faculties = Faculty.objects.filter(institution=institution)
    else:  # secondary
        departments = Department.objects.filter(institution=institution)
        faculties = None

    if request.method == 'POST':
        form = DepartmentForm(request.POST, institution_type=institution.type)
        if form.is_valid():
            department = form.save(commit=False)
            department.institution = institution
            if institution.type == 'higher':
                faculty_id = request.POST.get('faculty')
                department.faculty = get_object_or_404(Faculty, id=faculty_id)
            else:
                department.faculty = None  # Secondary profiles do not use faculty
            department.save()
            return redirect('manage_departments', institution_id=institution.id)
    else:
        form = DepartmentForm(institution_type=institution.type)

    # Dynamiczne wybieranie szablonu
    template_name = 'accounts/secondary/secondary_manage_departments.html' if institution.type == 'secondary' else 'accounts/higher/higher_manage_departments.html'

    return render(request, template_name, {
        'institution': institution,
        'departments': departments,
        'faculties': faculties,  # Przekazujemy listę wydziałów tylko dla higher
        'form': form,
    })


@login_required
def edit_department(request, institution_id, department_id):
    institution = get_object_or_404(Institution, id=institution_id)
    department = get_object_or_404(Department, id=department_id,
                                   faculty__institution=institution if institution.type == 'higher' else None)

    # Pobieramy listę wydziałów tylko dla 'higher'
    faculties = Faculty.objects.filter(institution=institution) if institution.type == 'higher' else None

    if request.method == 'POST':
        form = DepartmentForm(request.POST, instance=department, institution_type=institution.type)
        if form.is_valid():
            form.save()
            return redirect('manage_departments', institution_id=institution_id)
    else:
        form = DepartmentForm(instance=department, institution_type=institution.type)

    return render(request, 'departments/edit_department.html', {
        'form': form,
        'department': department,
        'institution': institution,
        'faculties': faculties,  # Przekazujemy listę wydziałów do szablonu
    })

@login_required
def delete_department(request, institution_id, department_id):
    institution = get_object_or_404(Institution, id=institution_id)
    department = get_object_or_404(Department, id=department_id, faculty__institution=institution if institution.type == 'higher' else None)

    department.delete()
    return redirect('manage_departments', institution_id=institution_id)

@login_required
def manage_faculties(request, institution_id):
    institution = get_object_or_404(Institution, id=institution_id)
    faculties = Faculty.objects.filter(institution=institution)

    if request.method == 'POST':
        form = FacultyForm(request.POST)
        if form.is_valid():
            faculty = form.save(commit=False)
            faculty.institution = institution
            faculty.save()
            return redirect('manage_faculties', institution_id=institution.id)
    else:
        form = FacultyForm()

    return render(request, 'accounts/higher/higher_manage_faculties.html', {
        'institution': institution,
        'faculties': faculties,
        'form': form,
    })

@login_required
def edit_faculty(request, institution_id, faculty_id):
    faculty = get_object_or_404(Faculty, id=faculty_id, institution_id=institution_id)

    if request.method == 'POST':
        form = FacultyForm(request.POST, instance=faculty)
        if form.is_valid():
            form.save()
            return redirect('manage_faculties', institution_id=institution_id)
    else:
        form = FacultyForm(instance=faculty)

    return render(request, 'faculties/edit_faculty.html', {
        'form': form,
        'faculty': faculty
    })

@login_required
def delete_faculty(request, institution_id, faculty_id):
    faculty = get_object_or_404(Faculty, id=faculty_id, institution_id=institution_id)
    faculty.delete()
    return redirect('manage_faculties', institution_id=institution_id)
