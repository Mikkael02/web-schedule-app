from django import forms
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from SubjectFrequency.forms import SubjectFrequencyFormSet
from institutions.models import Institution
from group.models import Group
from department.models import Department
from course.models import Course
from SubjectFrequency.models import SubjectFrequency
from collections import defaultdict

@login_required
def define_subject_frequency(request, institution_id):
    institution = get_object_or_404(Institution, id=institution_id)
    institution_type = institution.type

    grouped_forms = {}
    frequencies = SubjectFrequency.objects.filter(institution=institution)
    frequency_map = {(sf.group.id, sf.course.id): sf for sf in frequencies}

    if institution_type == 'primary':
        groups = Group.objects.filter(institution=institution).order_by('level')
        for group in groups:
            grouped_forms[f"Klasa {group.level}"] = [
                {
                    'group': group,
                    'course': course,
                    'frequency': frequency_map.get((group.id, course.id), None),
                }
                for course in Course.objects.filter(institution=institution)
            ]
    elif institution_type == 'secondary':
        departments = Department.objects.filter(institution=institution)
        for department in departments:
            grouped_forms[department.name] = {}
            for group in Group.objects.filter(department=department).order_by('level'):
                grouped_forms[department.name][f"Klasa {group.level}"] = [
                    {
                        'group': group,
                        'course': course,
                        'frequency': frequency_map.get((group.id, course.id), None),
                    }
                    for course in Course.objects.filter(institution=institution)
                ]
    elif institution_type == 'higher':
        departments = Department.objects.filter(faculty__institution=institution)
        for department in departments:
            grouped_forms[department.name] = {}
            for group in Group.objects.filter(department=department).order_by('level'):
                grouped_forms[department.name][f"Semestr {group.level}"] = [
                    {
                        'group': group,
                        'course': course,
                        'frequency': frequency_map.get((group.id, course.id), None),
                    }
                    for course in Course.objects.filter(institution=institution)
                ]

    if request.method == 'POST':
        SubjectFrequency.objects.filter(institution=institution).delete()
        for key, value in request.POST.items():
            if key.startswith("frequency-"):
                try:
                    _, group_id, course_id = key.split('-')
                    frequency = float(value)
                    group = Group.objects.get(id=group_id)
                    course = Course.objects.get(id=course_id)
                    shared_groups = request.POST.getlist(f"shared-{group_id}-{course_id}")
                    sf = SubjectFrequency.objects.create(
                        institution=institution,
                        group=group,
                        course=course,
                        frequency=frequency,
                    )
                    if shared_groups:
                        sf.shared_groups.set(Group.objects.filter(id__in=shared_groups))
                except Exception as e:
                    print(f"Błąd przetwarzania danych: {e}")
        return redirect('automatic_schedule', institution_id=institution_id)

    frequency_choices = [0] + [round(x * 0.5, 1) for x in range(1, 21)]

    return render(request, 'schedules/define_subject_frequency.html', {
        'institution': institution,
        'grouped_forms': grouped_forms,
        'frequency_choices': frequency_choices,
        'groups': Group.objects.filter(institution=institution),
    })
