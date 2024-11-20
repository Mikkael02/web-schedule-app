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

    formset_initial = []
    grouped_forms = {}

    if institution_type == 'primary':
        groups = Group.objects.filter(institution=institution).order_by('level')
        formset_initial = [
            {'group': group, 'course': course, 'institution': institution}
            for group in groups
            for course in Course.objects.filter(institution=institution)
        ]
        for group in groups:
            grouped_forms[f"Klasa {group.level}"] = [
                {'group': group, 'course': course}
                for course in Course.objects.filter(institution=institution)
            ]

    else:  # For secondary and higher
        departments = Department.objects.filter(faculty__institution=institution)
        for department in departments:
            department_groups = Group.objects.filter(department=department).order_by('level')
            grouped_forms[department.name] = {}
            for group in department_groups:
                grouped_forms[department.name][f"Klasa/Semestr {group.level}"] = [
                    {'group': group, 'course': course}
                    for course in Course.objects.filter(institution=institution)
                ]
                formset_initial.extend([
                    {'group': group, 'course': course, 'department': department, 'institution': institution}
                    for course in Course.objects.filter(institution=institution)
                ])

    # Tworzenie formsetu
    formset = SubjectFrequencyFormSet(
        request.POST or None,
        queryset=SubjectFrequency.objects.filter(institution=institution),
        initial=formset_initial
    )

    for form in formset:
        form.fields['course'].queryset = Course.objects.filter(institution=institution)

    if request.method == 'POST':
        if formset.is_valid():
            instances = formset.save(commit=False)
            for instance in instances:
                instance.institution = institution
                instance.save()
            return redirect('define_subject_frequency', institution_id=institution_id)

    frequency_choices = [0] + [round(x * 0.5, 1) for x in range(1, 21)]

    return render(request, 'schedules/define_subject_frequency.html', {
        'institution': institution,
        'grouped_forms': grouped_forms,
        'frequency_choices': frequency_choices,
    })
