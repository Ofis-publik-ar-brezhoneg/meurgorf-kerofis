from django_filters import rest_framework as filters

from .models import Location


class LocationFilter(filters.FilterSet):
    generic_name_contains = filters.CharFilter(field_name='generic_name', lookup_expr='icontains')
    generic_name_startswith = filters.CharFilter(field_name='generic_name', lookup_expr='istartswith')
    generic_name_endswith = filters.CharFilter(field_name='generic_name', lookup_expr='iendswith')
    generic_name_exact = filters.CharFilter(field_name='generic_name', lookup_expr='iexact')

    name_contains = filters.CharFilter(field_name='name', lookup_expr='icontains')
    name_startswith = filters.CharFilter(field_name='name', lookup_expr='istartswith')
    name_endswith = filters.CharFilter(field_name='name', lookup_expr='iendswith')
    name_exact = filters.CharFilter(field_name='name', lookup_expr='iexact')

    search_keyword_contains = filters.CharFilter(field_name='name', lookup_expr='icontains')
    search_keyword_startswith = filters.CharFilter(field_name='name', lookup_expr='istartswith')
    search_keyword_endswith = filters.CharFilter(field_name='name', lookup_expr='iendswith')
    search_keyword_exact = filters.CharFilter(field_name='name', lookup_expr='iexact')

    city_contains = filters.CharFilter(field_name='city__name', lookup_expr='icontains')
    city_startswith = filters.CharFilter(field_name='city__name', lookup_expr='istartswith')
    city_endswith = filters.CharFilter(field_name='city__name', lookup_expr='iendswith')
    city_exact = filters.CharFilter(field_name='city__name', lookup_expr='iexact')

    department_contains = filters.CharFilter(field_name='department__name', lookup_expr='icontains')
    department_startswith = filters.CharFilter(field_name='department__name', lookup_expr='istartswith')
    department_endswith = filters.CharFilter(field_name='department__name', lookup_expr='iendswith')
    department_exact = filters.CharFilter(field_name='department__name', lookup_expr='iexact')

    old_name_contains = filters.CharFilter(field_name='old_forms__old_form', lookup_expr='icontains')
    old_name_startswith = filters.CharFilter(field_name='old_forms__old_form', lookup_expr='istartswith')
    old_name_endswith = filters.CharFilter(field_name='old_forms__old_form', lookup_expr='iendswith')
    old_name_exact = filters.CharFilter(field_name='old_forms__old_form', lookup_expr='iexact')

    normalized_name_contains = filters.CharFilter(field_name='attested_forms__attested_form',
                                                  lookup_expr='icontains')
    normalized_name_startswith = filters.CharFilter(field_name='attested_forms__attested_form',
                                                    lookup_expr='istartswith')
    normalized_name_endswith = filters.CharFilter(field_name='attested_forms__attested_form',
                                                  lookup_expr='iendswith')
    normalized_name_exact = filters.CharFilter(field_name='attested_forms__attested_form',
                                               lookup_expr='iexact')

    standardized_name_contains = filters.CharFilter(field_name='standardized_forms__standardized_form',
                                                    lookup_expr='icontains')
    standardized_name_startswith = filters.CharFilter(field_name='standardized_forms__standardized_form',
                                                      lookup_expr='istartswith')
    standardized_name_endswith = filters.CharFilter(field_name='standardized_forms__standardized_form',
                                                    lookup_expr='iendswith')
    standardized_name_exact = filters.CharFilter(field_name='standardized_forms__standardized_form',
                                                 lookup_expr='iexact')

    class Meta:
        model = Location
        fields = [
            'category', 'generic_name_contains', 'generic_name_startswith', 'generic_name_endswith',
            'generic_name_exact', 'name_contains', 'name_startswith', 'name_endswith', 'name_exact',
            'search_keyword_contains', 'search_keyword_startswith', 'search_keyword_endswith', 'search_keyword_exact',
            'city_contains', 'city_startswith', 'city_endswith', 'city_exact', 'department_contains',
            'department_startswith', 'department_endswith', 'department_exact', 'old_name_contains',
            'old_name_startswith', 'old_name_endswith', 'old_name_exact', 'normalized_name_contains',
            'normalized_name_startswith', 'normalized_name_endswith', 'normalized_name_exact',
            'standardized_name_contains', 'standardized_name_startswith', 'standardized_name_endswith',
            'standardized_name_exact', 'city'
        ]
