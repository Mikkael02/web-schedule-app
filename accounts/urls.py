from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .forms import CustomAuthenticationForm
from .views import delete_account_confirm

urlpatterns = [
    path(
        'logowanie/',
        auth_views.LoginView.as_view(
            template_name='accounts/login.html',
            authentication_form=CustomAuthenticationForm
        ),
        name='login'
    ),
    path('wyloguj/', auth_views.LogoutView.as_view(), name='logout'),
    path('rejestracja/', views.register, name='register'),
    path('profil/', views.profile, name='profile'),
    path('ustawienia/', views.settings, name='settings'),
    path('usun-konto/', delete_account_confirm, name='delete_account'),
    path('plany/', views.plans, name='plans'),
    path('utworz_plan/', views.create_plan, name='create_plan'),
    path('plan/<int:plan_id>/', views.plan_detail, name='plan_detail'),
]
