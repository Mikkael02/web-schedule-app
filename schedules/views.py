from django.shortcuts import render
from .models import Schedule
from django.shortcuts import redirect
from .forms import ScheduleForm

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
