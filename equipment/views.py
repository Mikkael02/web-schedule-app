from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Equipment
from .forms import EquipmentForm

@login_required
def manage_equipment(request):
    equipment_list = Equipment.objects.filter(owner=request.user)

    if request.method == 'POST':
        form = EquipmentForm(request.POST)
        if form.is_valid():
            equipment = form.save(commit=False)
            equipment.owner = request.user
            equipment.save()
            return redirect('equipment:manage_equipment')
    else:
        form = EquipmentForm()

    return render(request, 'equipment/manage_equipment.html', {
        'equipment_list': equipment_list,
        'form': form
    })

@login_required
def edit_equipment(request, pk):
    equipment = get_object_or_404(Equipment, pk=pk, owner=request.user)

    if request.method == 'POST':
        form = EquipmentForm(request.POST, instance=equipment)
        if form.is_valid():
            form.save()
            return redirect('equipment:manage_equipment')
    else:
        form = EquipmentForm(instance=equipment)

    return render(request, 'equipment/edit_equipment.html', {'form': form})

@login_required
def delete_equipment(request, pk):
    equipment = get_object_or_404(Equipment, pk=pk, owner=request.user)
    equipment.delete()
    return redirect('equipment:manage_equipment')
