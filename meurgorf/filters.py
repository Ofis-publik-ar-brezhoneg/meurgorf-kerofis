from django_filters import rest_framework as filters

from .models import Term


class TermFilter(filters.FilterSet):
    term_contains = filters.CharFilter(field_name='canonic_form', lookup_expr='icontains')
    term_startswith = filters.CharFilter(field_name='canonic_form', lookup_expr='istartswith')
    term_endswith = filters.CharFilter(field_name='canonic_form', lookup_expr='iendswith')
    term_exact = filters.CharFilter(field_name='canonic_form', lookup_expr='iexact')
    historical_occurrence_contains = filters.CharFilter(field_name='historical_occurrences__occurence',
                                                        lookup_expr='icontains')
    historical_occurrence_startswith = filters.CharFilter(field_name='historical_occurrences__occurence',
                                                          lookup_expr='istartswith')
    historical_occurrence_endswith = filters.CharFilter(field_name='historical_occurrences__occurence',
                                                        lookup_expr='iendswith')
    historical_occurrence_exact = filters.CharFilter(field_name='historical_occurrences__occurence',
                                                        lookup_expr='iendswith')

    class Meta:
        model = Term
        fields = ['term_contains', 'term_startswith', 'term_endswith', 'term_exact', 'grammatical_category',
                  'historical_occurrences__book', 'id', 'historical_occurrence_contains',
                  'historical_occurrence_startswith', 'historical_occurrence_endswith', 'historical_occurrence_exact']
