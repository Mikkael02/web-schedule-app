from django.shortcuts import render, redirect
from .models import Room
from .forms import RoomForm

def room_list(request):
    rooms = Room.objects.all()  # Pobiera wszystkie obiekty Room z bazy danych
    return render(request, 'rooms/room_list.html', {'rooms': rooms})


def room_create(request):
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('room_list')
    else:
        form = RoomForm()
    return render(request, 'rooms/room_form.html', {'form': form})


def room_detail(request, pk):
    room = Room.objects.get(pk=pk)
    return render(request, 'rooms/room_detail.html', {'room': room})