import django_filters
from django_filters import CharFilter
from .models import *

class ExamFilter(django_filters.FilterSet):

    exam_code = CharFilter(field_name="exam_code", lookup_expr='icontains')

    class Meta:
        model = Exam
        fields =['exam_code',]
