from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import RoomType
from .forms import RoomTypeForm

@login_required
def manage_room_types(request):
    room_types = RoomType.objects.filter(owner=request.user)

    if request.method == 'POST':
        form = RoomTypeForm(request.POST)
        if form.is_valid():
            room_type = form.save(commit=False)
            room_type.owner = request.user
            room_type.save()
            return redirect('room_types:manage_room_types')
    else:
        form = RoomTypeForm()

    return render(request, 'room_types/manage_room_types.html', {
        'room_types': room_types,
        'form': form
    })

@login_required
def edit_room_type(request, pk):
    room_type = get_object_or_404(RoomType, pk=pk, owner=request.user)

    if request.method == 'POST':
        form = RoomTypeForm(request.POST, instance=room_type)
        if form.is_valid():
            form.save()
            return redirect('room_types:manage_room_types')
    else:
        form = RoomTypeForm(instance=room_type)

    return render(request, 'room_types/edit_room_type.html', {'form': form})

@login_required
def delete_room_type(request, pk):
    room_type = get_object_or_404(RoomType, pk=pk, owner=request.user)
    room_type.delete()
    return redirect('room_types:manage_room_types')
