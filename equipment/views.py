from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Equipment
from .forms import EquipmentForm

@login_required
def manage_equipment_rooms(request):
    equipment = Equipment.objects.filter(owner=request.user)

    if request.method == 'POST':
        form = EquipmentForm(request.POST)
        if form.is_valid():
            equip = form.save(commit=False)
            equip.owner = request.user
            equip.save()
            return redirect('equipment:manage_equipment_rooms')
    else:
        form = EquipmentForm()

    context = {
        'equipment': equipment,
        'form': form,
    }
    return render(request, 'equipment/manage_equipment_rooms.html', context)

@login_required
def manage_equipment_courses(request):
    equipment = Equipment.objects.filter(owner=request.user)

    if request.method == 'POST':
        form = EquipmentForm(request.POST)
        if form.is_valid():
            equip = form.save(commit=False)
            equip.owner = request.user
            equip.save()
            return redirect('equipment:manage_equipment_courses')
    else:
        form = EquipmentForm()

    context = {
        'equipment': equipment,
        'form': form,
    }
    return render(request, 'equipment/manage_equipment_courses.html', context)


@login_required
def edit_equipment(request, pk, context):
    equipment = get_object_or_404(Equipment, pk=pk, owner=request.user)
    if request.method == 'POST':
        form = EquipmentForm(request.POST, instance=equipment)
        if form.is_valid():
            form.save()
            if context == 'rooms':
                return redirect('equipment:manage_equipment_rooms')
            else:
                return redirect('equipment:manage_equipment_courses')
    else:
        form = EquipmentForm(instance=equipment)

    template_name = f'equipment/edit_equipment_{context}.html'
    return render(request, template_name, {'form': form, 'equipment': equipment})


@login_required
def delete_equipment(request, pk, context):
    equipment = get_object_or_404(Equipment, pk=pk, owner=request.user)
    equipment.delete()
    if context == 'rooms':
        return redirect('equipment:manage_equipment_rooms')
    else:
        return redirect('equipment:manage_equipment_courses')