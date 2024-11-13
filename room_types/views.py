from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import RoomType
from .forms import RoomTypeForm

@login_required
def manage_room_types_rooms(request):
    room_types = RoomType.objects.filter(owner=request.user)

    if request.method == 'POST':
        form = RoomTypeForm(request.POST)
        if form.is_valid():
            room_type = form.save(commit=False)
            room_type.owner = request.user
            room_type.save()
            return redirect('room_types:manage_room_types_rooms')
    else:
        form = RoomTypeForm()

    context = {
        'room_types': room_types,
        'form': form,
    }
    return render(request, 'room_types/manage_room_types_rooms.html', context)

@login_required
def manage_room_types_courses(request):
    room_types = RoomType.objects.filter(owner=request.user)

    if request.method == 'POST':
        form = RoomTypeForm(request.POST)
        if form.is_valid():
            room_type = form.save(commit=False)
            room_type.owner = request.user
            room_type.save()
            return redirect('room_types:manage_room_types_courses')
    else:
        form = RoomTypeForm()

    context = {
        'room_types': room_types,
        'form': form,
    }
    return render(request, 'room_types/manage_room_types_courses.html', context)

@login_required
def edit_room_type(request, pk, context):
    room_type = get_object_or_404(RoomType, pk=pk, owner=request.user)
    if request.method == 'POST':
        form = RoomTypeForm(request.POST, instance=room_type)
        if form.is_valid():
            form.save()
            if context == 'rooms':
                return redirect('room_types:manage_room_types_rooms')
            else:
                return redirect('room_types:manage_room_types_courses')
    else:
        form = RoomTypeForm(instance=room_type)

    template_name = f'room_types/edit_room_type_{context}.html'
    return render(request, template_name, {'form': form, 'room_type': room_type})


@login_required
def delete_room_type(request, pk, context):
    room_type = get_object_or_404(RoomType, pk=pk, owner=request.user)
    room_type.delete()
    if context == 'rooms':
        return redirect('room_types:manage_room_types_rooms')
    else:
        return redirect('room_types:manage_room_types_courses')
