from rest_framework import serializers
from .models import Faculty

class FacultySerializer(serializers.HyperlinkedModelSerializer):
    institution = serializers.StringRelatedField()  # To pokaże reprezentację stringową instytucji

    class Meta:
        model = Faculty
        fields = ['url', 'name', 'institution']
        extra_kwargs = {
            'url': {'view_name': 'faculties-detail', 'lookup_field': 'pk'}
        }
