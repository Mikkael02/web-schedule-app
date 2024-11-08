from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Equipment
from .forms import EquipmentForm

@login_required
def add_equipment(request):
    if request.method == 'POST':
        form = EquipmentForm(request.POST)
        if form.is_valid():
            equipment = form.save(commit=False)
            equipment.owner = request.user
            equipment.save()
            return redirect('manage_rooms', institution_id=request.session.get('institution_id'))
    else:
        form = EquipmentForm()
    return render(request, 'equipment/add_equipment.html', {'form': form})
