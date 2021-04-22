from django.db.models import Prefetch
from django.db.models import Q
from django.core.paginator import Paginator
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import TemplateView
from django.views.generic import View
from django.http import JsonResponse

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import ModelViewSet
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response

from commun.pagination import StandardPagination
from commun.pagination import AutoCompletePagination
from commun.views import ExportView
from commun.views import OldExportView
from commun.models import Book

from .models import DerivedForm
from .models import GrammaticalCategory
from .models import HistoricalOccurrence
from .models import PhoneticForm
from .models import Term
from .models import TermSearchQuery
from .models import Variant
from .forms import TermForm
from .serializers import DerivedFormSerializer
from .serializers import GrammaticalCategorySerializer
from .serializers import GrammaticalCategoryStatSerializer
from .serializers import HistoricalOccurrenceSerializer
from .serializers import TermSerializer
from .serializers import VariantSerializer
from .serializers import PhoneticFormSerializer
from .filters import TermFilter
from .utils import save_search_query


OPERATIONS = {
    "pm": "icontains",
    "me": "iexact",
    "dm": "istartswith",
    "fm": "iendswith"
}


def get_related(canonic_form):
    return reversed(
        Term.objects.filter(canonic_form__lt=canonic_form).order_by('-canonic_form')[:2]
    ), Term.objects.filter(canonic_form__gt=canonic_form).order_by('canonic_form')[:3]


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
            "phonetic_forms": PhoneticForm.objects.exclude(phonetic_form__isnull=True).count(),
            "phonetic_links": PhoneticForm.objects.exclude(phonetic_file__isnull=True).count(),
            "searchs": 0,
            "grammatical_categories": serializer.data
        })


class MeurgorfExportView(OldExportView):
    model = Term
    queryset = Term.objects.all()


class PhoneticFormView(ModelViewSet):
    serializer_class = PhoneticFormSerializer
    model = PhoneticForm
    queryset = PhoneticForm.objects.all()

####


class TermSearch(TemplateView):
    template_name = 'semantic/meurgorf/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = GrammaticalCategory.objects.all().order_by('title_fra')
        context['books'] = Book.objects.filter(is_meurgorf=True)
        context['terms_count'] = Term.objects.count()
        if self.request.POST:
            context['data'] = self.request.POST
        else:
            context['data'] = {
                'term': self.request.GET.get('search', ""),
                'search_type': self.request.GET.get("search_type", "me")}
        context['page'] = self.request.POST.get('page') or 1

        queryset = None
        if self.kwargs.get('term_id'):
            queryset = Term.objects.filter(pk=self.kwargs['term_id'])
        elif context['data'].get('term'):
            data = context['data']
            filters = {}
            operation = OPERATIONS.get(data.get('search_type'))
            term_filter = Q(**{f"canonic_form__unaccent__{operation}": data['term']})
            term_filter |= Q(**{f"variants__variant__unaccent__{operation}": data['term']})
            if data.get('category'):
                filters['grammatical_category'] = data['category']
            if data.get('book'):
                filters['historical_occurrences__book'] = data['book']
            queryset = Term.objects.filter(term_filter, **filters)
            save_search_query(data['term'], data.get('search_type'), queryset)
        elif context['data'].get('category') and context['data'].get('book'):
            data = context['data']
            filters = {
                'grammatical_category': data['category'],
                'historical_occurrences__book': data['book']
            }
            queryset = Term.objects.filter(**filters)

        context['search_queries'] = TermSearchQuery.objects.order_by('-date')[:5]

        if queryset is not None:
            paginator = Paginator(queryset.order_by('canonic_form', 'pk').distinct('canonic_form', 'pk'), 20)
            context['paginator'] = paginator
            context['terms'] = paginator.get_page(context['page'])
            context['related_terms'] = get_related(queryset.first().canonic_form) if queryset else None

        return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)


class SkridaozerMeurgorfTermView(TemplateView):
    template_name = 'semantic/skridaozer/meurgorf/etrefas.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = GrammaticalCategory.objects.all().order_by('title_bre')
        context['books'] = Book.objects.all().order_by('abbrevation')
        context['term_id'] = kwargs.get('term_id', 0)
        if kwargs.get('term_id'):
            context['term'] = Term.objects.get(pk=kwargs['term_id'])
            context['related_terms'] = get_related(context['term'].canonic_form)

        return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        data = self.request.POST

        if kwargs.get('term_id'):
            form = TermForm(self.request.POST, instance=context['term'])
            if form.is_valid():
                form.save()
            else:
                print(form.errors)
        else:
            category = GrammaticalCategory.objects.get(pk=data['grammatical_category'])
            obj = Term(canonic_form=data['canonic_form'], grammatical_category=category)
            obj.save()
            return redirect(reverse('skridaozer:meurgorf_etrefas', kwargs={'term_id': obj.id}))

        return self.render_to_response(context)


class SkridaozerMeurgorfStatView(TemplateView):
    template_name = 'semantic/skridaozer/meurgorf/stadegou.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['stats'] = {
            "Pennger en diaz": Term.objects.count(),
            "Stumm istorel testeniekaet": HistoricalOccurrence.objects.count(),
            "Adpennger": Variant.objects.count(),
            "Stumm deveret skouer": DerivedForm.objects.count(),
            "Stumm deveret all": DerivedForm.objects.exclude(sub_order__gt=0).count(),
            "Termenadur": Term.objects.exclude(definition__isnull=True).exclude(definition__exact='').count(),
            "Displegadur gerdarzhel": Term.objects.exclude(etymology__isnull=True).exclude(etymology__exact='').count(),
            "Notenn studiañ": Term.objects.exclude(study_notes__isnull=True).exclude(study_notes__exact='').count(),
            "Distagadur": PhoneticForm.objects.exclude(phonetic_form__isnull=True).count(),
            "Distagadur enrolladenn": PhoneticForm.objects.exclude(phonetic_file__isnull=True).count(),
            "Reket": 0
        }

        queryset = GrammaticalCategory.objects.all()
        kwargs = {
            'context': {'request': self.request},
            'many': True
        }
        context["grammatical_categories"] = GrammaticalCategoryStatSerializer(queryset, **kwargs).data

        return context


class SkridaozerMeurgorfExportView(ExportView):
    model = Term


class SkridaozerMeurgorfSearchView(TemplateView):
    template_name = 'semantic/skridaozer/meurgorf/klask.html'

    def get_context_data(self, **kwargs):
        queryset = None

        context = super().get_context_data(**kwargs)
        context['categories'] = GrammaticalCategory.objects.all().order_by('title_bre')
        context['books'] = Book.objects.exclude(title='').order_by('title')

        if self.request.POST:
            context['data'] = self.request.POST
            context['page'] = self.request.POST.get('page') or 1
            data = context['data']
            filters = {}
            operation = data.get('search_type')
            term_filter = Q(**{f"canonic_form__unaccent__{operation}": data['canonic_form']})
            term_filter |= Q(**{f"variants__variant__unaccent__{operation}": data['canonic_form']})
            if data.get('historical_occurrence'):
                filters['historical_occurrences__occurence'] = data['historical_occurrence']
            if data.get('category'):
                filters['grammatical_category'] = data['category']
            if data.get('book'):
                filters['historical_occurrences__book'] = data['book']
            queryset = Term.objects.filter(term_filter, **filters)
            paginator = Paginator(queryset.order_by('canonic_form', 'pk').distinct('canonic_form', 'pk'), 20)
            context['paginator'] = paginator
            context['terms'] = paginator.get_page(context['page'])
            context['related_terms'] = get_related(queryset.first().canonic_form) if queryset else None
        else:
            context['data'] = {'search_type': 'istartswith'}

        return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)


class SkridaozerMeurgorfAjaxView(View):

    def post(self, request, *args, **kwargs):
        try:
            action = request.POST.get('action')
            obj = Term.objects.get(pk=kwargs['term_id'])
            getattr(self, action)(obj, request.POST)

            return JsonResponse({"response": "ok"})
        except Exception as e:
            return JsonResponse({"response": "error", "msg": str(e)})

    def get(self, request, *args, **kwargs):
        results = []
        if request.GET.get('query'):
            for term in Term.objects.filter(canonic_form__icontains=request.GET.get('query', '')):
                results.append({
                    'id': term.id,
                    'title': term.canonic_form,
                    'description': term.grammatical_category.title_bre
                })
        return JsonResponse({'results': results})

    def add_variant(self, obj, data):
        variant = Variant(
            term=obj,
            variant=data['variant']
        )
        variant.save()

    def add_derived_form(self, obj, data):
        derived_form = DerivedForm(
            term=obj,
            order=1,
            sub_order=1,
            form=data['form']
        )
        derived_form.save()

    def add_phonetic_form(self, obj, data):
        phonetic_form = PhoneticForm(
            term=obj,
            phonetic_form=data['phonetic_form'],
            phonetic_file=data['phonetic_file']
        )
        phonetic_form.save()

    def add_parent(self, obj, data):
        obj.parents.add(data['id'])

    def add_historical_occurrence(self, obj, data):
        historical_occurrence = HistoricalOccurrence(
            occurence=data['occurence'],
            occurence_normalized=data['occurence_normalized'],
            litteral_year=data['litteral_year'],
            year=data['year'],
            book=Book.objects.get(pk=data['book']),
            reference=data['reference'],
        )
        historical_occurrence.save()
        historical_occurrence.terms.add(obj)

    def delete_variant(self, obj, data):
        Variant.objects.get(term=obj, pk=data['id']).delete()

    def delete_derived_form(self, obj, data):
        DerivedForm.objects.get(term=obj, pk=data['id']).delete()

    def delete_phonetic_form(self, obj, data):
        PhoneticForm.objects.get(term=obj, pk=data['id']).delete()

    def delete_parent(self, obj, data):
        obj.parents.remove(Term.objects.get(pk=data['id']))

    def delete_historical_occurrence(self, obj, data):
        historical_occurrence = HistoricalOccurrence.objects.get(pk=data['id'])
        obj.historical_occurrences.remove(historical_occurrence)
        historical_occurrence.delete()
