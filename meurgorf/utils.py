from django.utils import timezone
from .models import TermSearchQuery


def save_search_query(query, search_type, queryset):
    if not query.isalnum():
        return

    search_query, _ = TermSearchQuery.objects.get_or_create(query=query, defaults={
        'query_type': search_type,
        'counter': 0,
        'results_number': 0,
        'date': timezone.now()})
    search_query.date = timezone.now()
    search_query.counter += 1
    search_query.results_number = len(queryset)
    search_query.save()
