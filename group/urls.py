from django.urls import path
from .views import GroupListView, GroupCreateView, GroupUpdateView, GroupDeleteView

urlpatterns = [
    path('', GroupListView.as_view(), name='group_list'),
    path('create/', GroupCreateView.as_view(), name='group_create'),
    path('update/<int:pk>/', GroupUpdateView.as_view(), name='group_update'),
    path('delete/<int:pk>/', GroupDeleteView.as_view(), name='group_delete'),
]
