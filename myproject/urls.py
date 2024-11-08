"""
URL configuration for myproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls.py import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls.py'))
"""
from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('rooms/', include('rooms.urls')),
    path('teachers/', include('teachers.urls')),
    path('schedules/', include('schedules.urls')),
    path('courses/', include('course.urls')),
    path('groups/', include('group.urls')),
    path('institutions/', include('institutions.urls')),
    path('', include('faculty.urls')),
    path('', include('institutions.urls')),
    path('accounts/', include('accounts.urls')),
    path('api/', include('schedules.urls')),
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('room-types/', include('room_types.urls')),
    path('equipment/', include('equipment.urls')),
]
