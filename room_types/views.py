from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import RoomType
from .forms import RoomTypeForm

@login_required
def add_room_type(request):
    if request.method == 'POST':
        form = RoomTypeForm(request.POST)
        if form.is_valid():
            room_type = form.save(commit=False)
            room_type.owner = request.user
            room_type.save()
            return redirect('manage_rooms', institution_id=request.session.get('institution_id'))
    else:
        form = RoomTypeForm()
    return render(request, 'room_types/add_room_type.html', {'form': form})
