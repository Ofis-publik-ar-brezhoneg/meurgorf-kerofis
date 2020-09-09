from django.db.models import Prefetch
from django.core.paginator import Paginator
from django.views.generic import TemplateView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import ModelViewSet
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response

from commun.pagination import StandardPagination
from commun.pagination import AutoCompletePagination
from commun.views import ExportView
from commun.models import Book

from .models import DerivedForm
from .models import GrammaticalCategory
from .models import HistoricalOccurrence
from .models import PhoneticForm
from .models import Term
from .models import Variant
from .serializers import DerivedFormSerializer
from .serializers import GrammaticalCategorySerializer
from .serializers import GrammaticalCategoryStatSerializer
from .serializers import HistoricalOccurrenceSerializer
from .serializers import TermSerializer
from .serializers import VariantSerializer
from .filters import TermFilter


OPERATIONS = {
    "pm": "icontains",
    "me": "iexact",
    "dm": "istartswith",
    "fm": "iendwith"
}


class GrammaticalCategoryView(ModelViewSet):
    serializer_class = GrammaticalCategorySerializer
    model = GrammaticalCategory
    queryset = GrammaticalCategory.objects.all()


class TermView(ModelViewSet):
    serializer_class = TermSerializer
    model = Term
    queryset = Term.objects.prefetch_related(
        Prefetch('derived_forms', queryset=DerivedForm.objects.order_by('order', 'sub_order')))
    filter_backends = (DjangoFilterBackend, )
    filterset_class = TermFilter
    pagination_class = StandardPagination

    @property
    def paginator(self):
        """
        Reduce the paginator in case of autocomplete request
        """
        if not hasattr(self, '_paginator'):
            if 'autocomplete' in self.request.GET:
                self._paginator = AutoCompletePagination()
            else:
                self._paginator = self.pagination_class()

        return self._paginator


class VariantView(ModelViewSet):
    serializer_class = VariantSerializer
    model = Variant
    queryset = Variant.objects.all()


class DerivedFormView(ModelViewSet):
    serializer_class = DerivedFormSerializer
    model = DerivedForm
    queryset = DerivedForm.objects.all()


class HistoricalOccurrenceView(ModelViewSet):
    serializer_class = HistoricalOccurrenceSerializer
    model = HistoricalOccurrence
    queryset = HistoricalOccurrence.objects.all()


class StatView(GenericViewSet):
    serializer_class = GrammaticalCategoryStatSerializer
    model = GrammaticalCategory
    queryset = GrammaticalCategory.objects.all()

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)

        return Response({
            "terms": Term.objects.count(),
            "historical_occurences": HistoricalOccurrence.objects.count(),
            "variants": Variant.objects.count(),
            "derived_forms": DerivedForm.objects.count(),
            "principal_derived_forms": DerivedForm.objects.exclude(sub_order__gt=0).count(),
            "definitions": Term.objects.exclude(definition__isnull=True).exclude(definition__exact='').count(),
            "etymologies": Term.objects.exclude(etymology__isnull=True).exclude(etymology__exact='').count(),
            "study_notes": Term.objects.exclude(study_notes__isnull=True).exclude(study_notes__exact='').count(),
            "phonetic_forms": PhoneticForm.objects.exclude(phonetic_form__isnull=True).
                exclude(phonetic_form__exact='').count(),
            "phonetic_links": PhoneticForm.objects.exclude(url__isnull=True).
                exclude(url__exact='').count(),
            "searchs": 0,
            "grammatical_categories": serializer.data
        })


class MeurgorfExportView(ExportView):
    model = Term
    queryset = Term.objects.all()


class TermSearch(TemplateView):
    template_name = 'semantic/meurgorf/index.html'

    def get_context_data(self, term_id=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = GrammaticalCategory.objects.all()
        context['books'] = Book.objects.filter(is_meurgorf=True)
        context['data'] = self.request.POST
        context['page'] = self.request.POST.get('page') or 1

        queryset = None
        if term_id:
            queryset = Term.objects.filter(pk=term_id)
        elif context['data'].get('term'):
            data = context['data']
            filters = {
                f"canonic_form__{OPERATIONS.get(data.get('search_type'))}": data['term']
            }
            if data.get('category'):
                filters['grammatical_category'] = data['category']
            if data.get('book'):
                filters['historical_occurrences__book'] = data['book']
            queryset = Term.objects.filter(**filters)

        if queryset:
            paginator = Paginator(queryset, 5)
            context['paginator'] = paginator
            context['terms'] = paginator.get_page(context['page'])

        return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)