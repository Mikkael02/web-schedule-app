from django.shortcuts import render, get_object_or_404, redirect
from .models import TimeConfiguration
from institutions.models import Institution
from .forms import TimeConfigurationForm
from django.contrib.auth.decorators import login_required

@login_required
def configure_time(request, institution_id):
    institution = get_object_or_404(Institution, id=institution_id)
    time_config, created = TimeConfiguration.objects.get_or_create(institution=institution)

    if request.method == 'POST':
        form = TimeConfigurationForm(request.POST, instance=time_config)
        if form.is_valid():
            form.save()
            return redirect('generate_schedule', institution_id=institution.id)
    else:
        form = TimeConfigurationForm(instance=time_config)

    return render(request, 'time_configuration/configure_time.html', {
        'institution': institution,
        'form': form,
    })
