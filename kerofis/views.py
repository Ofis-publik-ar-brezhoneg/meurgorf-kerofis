from django.core.paginator import Paginator
from django.db.models import Count
from django.views.generic import TemplateView
from django.views.generic import RedirectView
from django.urls import reverse

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import ModelViewSet
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response

from commun.pagination import StandardPagination
from commun.pagination import AutoCompletePagination
from commun.views import ExportView

from .models import Category
from .models import City
from .models import Department
from .models import Location
from .models import Informant
from .models import PhoneticTranscription
from .models import StandardizedForm
from .models import OldForm
from .models import AttestedForm
from .models import OtherForm
from .models import TermSearchQuery
from .models import PhoneticTranscriptionLink
from .filters import LocationFilter
from .serializers import LocationSerializer
from .serializers import LocationCategorySerializer
from .serializers import InformantSerializer
from .serializers import CategoryStatSerializer
from .serializers import CitySerializer
from .serializers import StandardizedFormSerializer
from .serializers import PhoneticTranscriptionsSerializer
from .serializers import OldFormsSerializer
from .serializers import OtherFormsSerializer
from .serializers import AttestedFormSerializer

OPERATIONS = {
    "pm": "icontains",
    "me": "iexact",
    "dm": "istartswith",
    "fm": "iendswith"
}


class KerofisSearch(TemplateView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['nb_location'] = Location.objects.count()
        context['categories'] = Category.objects.all().order_by('name_fra')
        context['cities'] = City.objects.all().order_by('name_fra')
        context['departments'] = Department.objects.all().order_by('name_fra')
        if self.request.POST:
            context['data'] = self.request.POST
        else:
            context['data'] = {'name': self.request.GET.get('search', ""), 'search_type': 'me'}
        context['page'] = self.request.POST.get('page') or 1

        queryset = None
        if self.kwargs.get('location_id'):
            queryset = Location.objects.filter(pk=self.kwargs['location_id'])
        elif self.request.POST.get('name'):
            data = self.request.POST
            operation = OPERATIONS.get(data.get('search_type'))
            queryset = Location.objects.filter(**{f'name__unaccent__{operation}': data.get('name')})

        if queryset is not None:
            paginator = Paginator(queryset.order_by('name', 'pk').distinct('name', 'pk'), 20)
            context['paginator'] = paginator
            context['locations'] = paginator.get_page(context['page'])

        return context

    def get_template_names(self):
        print(self.request.POST.get('name'))
        if self.request.POST.get('name'):
            return ['semantic/kerofis/search.html']

        if self.kwargs.get('location_id'):
            return ['semantic/kerofis/location.html']

        return ['semantic/kerofis/index.html']

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)


class KerofisRedirect(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        """
        Return the URL redirect to. Keyword arguments from the URL pattern
        match generating the redirect request are provided as kwargs to this
        method.
        """
        location_id = None
        location_name = kwargs.get('location_name')
        if location_name:
            print(Location.objects.filter(name=location_name).all())
            location_id = Location.objects.filter(name=location_name, category__name_fra='Commune').first().id

        return reverse('kerofis', kwargs={'location_id': location_id})


class LocationCategoryView(ModelViewSet):
    serializer_class = LocationCategorySerializer
    model = Category
    queryset = Category.objects.all()


class LocationView(ModelViewSet):
    serializer_class = LocationSerializer
    model = Location
    queryset = Location.objects.all()
    filter_backends = (DjangoFilterBackend, )
    filterset_class = LocationFilter
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


class InformantView(ModelViewSet):
    serializer_class = InformantSerializer
    model = Informant
    queryset = Informant.objects.all()


class KerofisStatView(GenericViewSet):
    serializer_class = CategoryStatSerializer
    model = Category
    queryset = Category.objects.all()

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)

        return Response({
            "locations": Location.objects.count(),
            "phonetic_transcription": PhoneticTranscription.objects.count(),
            "locations_with_phonetic": Location.objects.filter(phonetic_transcriptions__isnull=False).count(),
            "normalized_forms": StandardizedForm.objects.count(),
            "public_locations": Location.objects.filter(is_public=True).count(),
            "old_forms": OldForm.objects.count(),
            "attested_forms": AttestedForm.objects.count(),
            "other_forms": OtherForm.objects.count(),
            "has_coordinates": Location.objects.filter(longitude__isnull=False).count(),
            "has_formalized_date": Location.objects.filter(formalized_date__isnull=False).count(),
            "is_on_ign": Location.objects.filter(on_ign=True).count(),
            "etymological_note_fra": Location.objects.filter(etymological_note_fra__isnull=False).count(),
            "etymological_note_bre": Location.objects.filter(etymological_note_bre__isnull=False).count(),
            "nb_query": TermSearchQuery.objects.count(),
            "standard_phonetic": PhoneticTranscription.objects.filter(is_standard=True).count(),
            "phonetic_links": PhoneticTranscriptionLink.objects.count(),
            "by_department": Location.objects.values('department__name_bre').annotate(locations_count=Count('id')),
            "categories": serializer.data
        })


class KerofisExportView(ExportView):
    model = Location
    queryset = Location.objects.all()


class CityView(ModelViewSet):
    serializer_class = CitySerializer
    model = City
    queryset = City.objects.all()


class StandardizedFormView(ModelViewSet):
    serializer_class = StandardizedFormSerializer
    model = StandardizedForm
    queryset = StandardizedForm.objects.all()


class PhoneticTranscriptionView(ModelViewSet):
    serializer_class = PhoneticTranscriptionsSerializer
    model = PhoneticTranscription
    queryset = PhoneticTranscription.objects.all()


class OldFormView(ModelViewSet):
    serializer_class = OldFormsSerializer
    model = OldForm
    queryset = OldForm.objects.all()


class OtherFormView(ModelViewSet):
    serializer_class = OtherFormsSerializer
    model = OtherForm
    queryset = OtherForm.objects.all()


class AttestedFormView(ModelViewSet):
    serializer_class = AttestedFormSerializer
    model = AttestedForm
    queryset = AttestedForm.objects.all()
