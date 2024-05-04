from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Group
from .forms import GroupForm

class GroupListView(ListView):
    model = Group
    context_object_name = 'groups'

class GroupCreateView(CreateView):
    model = Group
    form_class = GroupForm
    success_url = reverse_lazy('group_list')

class GroupUpdateView(UpdateView):
    model = Group
    form_class = GroupForm
    success_url = reverse_lazy('group_list')

class GroupDeleteView(DeleteView):
    model = Group
    success_url = reverse_lazy('group_list')
