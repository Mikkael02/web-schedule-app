# faculties/views.py
from rest_framework.generics import ListAPIView
from .models import Faculty
from .serializers import FacultySerializer
from rest_framework.generics import RetrieveAPIView

class FacultyListView(ListAPIView):
    queryset = Faculty.objects.all()
    serializer_class = FacultySerializer

class FacultyDetailView(RetrieveAPIView):
    queryset = Faculty.objects.all()
    serializer_class = FacultySerializer