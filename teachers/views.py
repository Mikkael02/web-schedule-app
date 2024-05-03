from django.shortcuts import render
from .models import Teacher
from django.shortcuts import redirect
from .forms import TeacherForm

def teacher_list(request):
    teachers = Teacher.objects.all()  # Pobiera wszystkie obiekty Teacher z bazy danych
    return render(request, 'teachers/teacher_list.html', {'teachers': teachers})

def teacher_create(request):
    if request.method == 'POST':
        form = TeacherForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('teacher_list')
    else:
        form = TeacherForm()
    return render(request, 'teachers/teacher_form.html', {'form': form})

def teacher_detail(request, pk):
    teacher = Teacher.objects.get(pk=pk)
    return render(request, 'teachers/teacher_detail.html', {'teacher': teacher})
