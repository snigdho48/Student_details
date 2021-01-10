import django_filters
from django_filters import DateFilter

from .models import *


class DataFilter(django_filters.FilterSet):
    class Meta:
        model = Student
        fields = '__all__'
