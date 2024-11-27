from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, UserUpdateForm, CustomPasswordChangeForm
from institutions.models import Institution
from django.shortcuts import get_object_or_404
from django.contrib.auth import update_session_auth_hash

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Rejestracja zakończona sukcesem.')
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})

@login_required
def delete_account_confirm(request):
    if request.method == 'POST':
        user = request.user
        user.delete()
        messages.success(request, "Twoje konto zostało usunięte.")
        return redirect('home')
    return render(request, 'accounts/delete_account_confirm.html')

@login_required
def profile(request):
    return render(request, 'accounts/profile.html')

@login_required
def settings(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        password_form = CustomPasswordChangeForm(user=request.user, data=request.POST)

        if user_form.is_valid():
            user_form.save()
            messages.success(request, "Twoje dane zostały zaktualizowane.")
            return redirect('settings')
        elif password_form.is_valid():
            password_form.save()
            update_session_auth_hash(request, password_form.user)
            messages.success(request, "Hasło zostało zmienione.")
            return redirect('settings')
        else:
            messages.error(request, "Wystąpił błąd podczas aktualizacji danych.")
    else:
        user_form = UserUpdateForm(instance=request.user)
        password_form = CustomPasswordChangeForm(user=request.user)

    return render(request, 'accounts/settings.html', {
        'user_form': user_form,
        'password_form': password_form
    })

@login_required
def plans(request):
    user_plans = Institution.objects.filter(owner=request.user)
    return render(request, 'accounts/plans.html', {'plans': user_plans})

@login_required
def create_plan(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        institution_type = request.POST.get('type')
        logo = request.FILES.get('logo')

        if not name or not institution_type:
            messages.error(request, 'Proszę wypełnić wszystkie wymagane pola.')
            return render(request, 'accounts/create_plan.html')

        Institution.objects.create(name=name, type=institution_type, logo=logo, owner=request.user)
        messages.success(request, 'Plan został pomyślnie utworzony.')
        return redirect('plans')

    return render(request, 'accounts/create_plan.html')

@login_required
def plan_detail(request, plan_id):
    plan = get_object_or_404(Institution, id=plan_id, owner=request.user)
    return render(request, 'accounts/plan_detail.html', {'plan': plan})
