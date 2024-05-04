from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Course
from .forms import CourseForm

class CourseListView(ListView):
    model = Course
    context_object_name = 'courses'

class CourseCreateView(CreateView):
    model = Course
    form_class = CourseForm
    success_url = reverse_lazy('course_list')

class CourseUpdateView(UpdateView):
    model = Course
    form_class = CourseForm
    success_url = reverse_lazy('course_list')

class CourseDeleteView(DeleteView):
    model = Course
    success_url = reverse_lazy('course_list')
