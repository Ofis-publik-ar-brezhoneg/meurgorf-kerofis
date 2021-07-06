import random

from django.core.paginator import Paginator
from django.db.models import Count
from django.views.generic import TemplateView
from django.views.generic import RedirectView
from django.views.generic import View
from django.urls import reverse
from django.shortcuts import redirect
from django.shortcuts import render
from django.http import JsonResponse

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import ModelViewSet
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response

from commun.pagination import StandardPagination
from commun.pagination import AutoCompletePagination
from commun.views import ExportView
from commun.models import Book

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
from .forms import LocationForm
from .serializers import LocationSerializer
from .serializers import CategoryStatSerializer


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
        else:
            locations_of_day = list(Location.objects.filter(is_name_of_day=True).all())
            if len(locations_of_day):
                context['location_of_day'] = locations_of_day[random.randint(0, len(locations_of_day) - 1)]

        return context

    def get_template_names(self):
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


class SkridaozerKerofisLocationView(TemplateView):
    template_name = 'semantic/skridaozer/kerofis/etrefas.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['location_id'] = self.kwargs.get('location_id', '0')
        context['cities'] = City.objects.all().order_by('name_bre')
        context['categories'] = Category.objects.all().order_by('name_bre')
        context['informants'] = Informant.objects.all().order_by('first_name', 'last_name')
        context['books'] = Book.objects.all().order_by('abbrevation')
        context['books_old'] = Book.objects.filter(is_kerofis_old=True).order_by('abbrevation')

        if self.kwargs.get('location_id'):
            context['location'] = Location.objects.get(pk=self.kwargs['location_id'])

        return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        data = self.request.POST

        if self.kwargs.get('location_id'):
            form = LocationForm(self.request.POST, instance=context['location'])
            if form.is_valid():
                form.save()
            else:
                print(form.errors)
        else:
            obj = Location(generic_name=data['generic_name'], name=data['name'], created_by=self.request.user)
            obj.save()
            return redirect(reverse('skridaozer:kerofis_etrefas', kwargs={'location_id': obj.id}))

        return self.render_to_response(context)


class SkridaozerKerofisAddLocationView(RedirectView):
    pattern_name = 'skridaozer:kerofis_etrefas'

    def get_redirect_url(self, *args, **kwargs):
        location = Location(name=self.request.GET['name'], generic_name=self.request.GET['generic_name'])
        location.save()

        return super().get_redirect_url(location_id=location.id)


class SkridaozerKerofisStatView(TemplateView):
    template_name = 'semantic/skridaozer/kerofis/stadegou.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['stats_1'] = {
            "enrolladenn  en  diaz": [
                Location.objects.count(),
                ''
            ],
            "distagadur evit": [
                PhoneticTranscription.objects.count(),
                "{} anv-lec'h".format(Location.objects.filter(phonetic_transcriptions__isnull=False).count())
            ],
            "stumm skoueriekaet": [
                StandardizedForm.objects.count(),
                "{} %".format(round((StandardizedForm.objects.count() / Location.objects.count()) * 100, 2))
            ],
            "Aotre da embann": ['', ''],
            "Lec'hanvadurezh": [
                Location.objects.filter(is_public=True).count(),
                "{} %".format(
                    round((Location.objects.filter(is_public=True).count() / Location.objects.count()) * 100, 2)
                )
            ]
        }

        context['stats_2'] = {
            "stumm kozh testeniekaet": OldForm.objects.count(),
            "stumm  brezhoneg  testeniekaet": AttestedForm.objects.count(),
            "stumm all implijet": OtherForm.objects.count(),
            "daveenn douaroniel": Location.objects.filter(longitude__isnull=False).count(),
            "deiziad ofisielisaet": Location.objects.filter(formalized_date__isnull=False).count(),
            "ign": Location.objects.filter(on_ign=True).count(),
            "gerdarzh fra": Location.objects.filter(etymological_note_fra__isnull=False).count(),
            "gerdarzh bre": Location.objects.filter(etymological_note_bre__isnull=False).count(),
            "goulenn": TermSearchQuery.objects.count(),
            "distagadur skouer": PhoneticTranscription.objects.filter(is_standard=True).count(),
            "distagadur enrolladenn": PhoneticTranscriptionLink.objects.count()
        }

        context["dep"] = Location.objects.values('department__name_bre').annotate(locations_count=Count('id'))

        queryset = Category.objects.all()
        kwargs = {
            'context': {'request': self.request},
            'many': True
        }
        context["categories"] = CategoryStatSerializer(queryset, **kwargs).data

        return context


class SkridaozerKerofisExportView(ExportView):
    model = Location


class SkridaozerKerofisSearchView(TemplateView):
    template_name = 'semantic/skridaozer/kerofis/klask.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all().order_by('name_bre')
        context['departments'] = Department.objects.all().order_by('name_bre')

        if self.request.POST:
            context['data'] = self.request.POST
            context['page'] = self.request.POST.get('page') or 1
            data = context['data']
            filters = {}
            operation = data.get('search_type')
            if data.get('generic_name'):
                filters[f"generic_name__unaccent__{operation}"] = data['generic_name']
            if data.get('name'):
                if data.get('is_old'):
                    filters[f"old_forms__old_form__unaccent__{operation}"] = data['name']
                elif data.get('is_standardized'):
                    filters[f"standardized_forms__standardized_form__unaccent__{operation}"] = data['name']
                elif data.get('is_attested'):
                    filters[f"attested_forms__attested_form__unaccent__{operation}"] = data['name']
                else:
                    filters[f"name__unaccent__{operation}"] = data['name']
            if data.get('city'):
                filters[f"city__name_bre__unaccent__{operation}"] = data['city']
            if data.get('department'):
                filters['department'] = data['department']
            if data.get('category'):
                filters['category'] = data['category']

            sorting = self.request.POST.get('sorting_field', 'generic_name')
            if self.request.POST.get('sorting_order') == 'desc':
                sorting = f'-{sorting}'

            context['locations'] = Location.objects.filter(**filters)
        else:
            context['data'] = {'search_type': 'icontains'}

        context['sorting_field'] = self.request.POST.get('sorting_field', 'generic_name')
        context['sorting_order'] = self.request.POST.get('sorting_order', 'asc')
        context['sorting_label'] = 'descending' if self.request.POST.get('sorting_order') == 'desc' else 'ascending'

        return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)


class SkridaozerKerofisInformantView(TemplateView):
    template_name = 'semantic/skridaozer/kerofis/titourer.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['informants'] = Informant.objects.all().order_by('id')

        if self.kwargs.get('informant_id'):
            context['data'] = Informant.objects.get(pk=self.kwargs['informant_id'])

        return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        obj = context['data']
        data = self.request.POST
        obj.first_name = data.get('first_name')
        obj.last_name = data.get('last_name')
        obj.surname = data.get('surname')
        obj.occupation = data.get('occupation')
        obj.birthdate = data.get('birthdate')
        obj.birthplace = data.get('birthplace')
        obj.cities = data.get('cities')
        obj.arrival_date = data.get('arrival_date')
        obj.notes = data.get('notes')
        obj.contact = data.get('contact')
        obj.interviewed_by = self.request.user
        obj.save()

        context['data'] = obj

        return self.render_to_response(context)


class SkridaozerKerofisExportInfoView(TemplateView):
    template_name = 'semantic/skridaozer/kerofis/levrigou.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cities'] = City.objects.all()

        return context


class SkridaozerKerofisAjaxView(View):

    def post(self, request, *args, **kwargs):
        try:
            action = request.POST.get('action')
            obj = Location.objects.get(pk=self.kwargs['location_id'])
            getattr(self, action)(obj, request.POST)

            return JsonResponse({"response": "ok"})
        except Exception as e:
            return JsonResponse({"response": "error", "msg": str(e)})

    def delete(self, request, *args, **kwargs):
        try:
            Location.objects.filter(pk=self.kwargs['location_id']).delete()
            return JsonResponse({"response": "ok"})
        except Exception as e:
            return JsonResponse({"response": "error", "msg": str(e)})

    def add_standardized_form(self, obj, data):
        form = StandardizedForm(standardized_form=data['form'], date=data['date'], location=obj)
        form.save()

    def add_phonetic_transcription(self, obj, data):
        phonetic_transcription = PhoneticTranscription(
            location=obj,
            phonetic_transcription=data['phonetic_transcription'],
            is_standard=data['is_standard'] == 'true',
            informant=Informant.objects.get(pk=data['informant']),
            created_at=data['created_at']
        )
        phonetic_transcription.save()
        phonetic_transcription_link = PhoneticTranscriptionLink(phonetic_transcription=phonetic_transcription, link=data['link'])
        phonetic_transcription_link.save()

    def add_old_form(self, obj, data):
        old_form = OldForm(
            location=obj,
            old_form=data['old_form'],
            litteral_year=data['litteral_year'],
            year=data['year'],
            book=Book.objects.get(pk=data['book']),
            reference=data['reference']
        )
        old_form.save()

    def add_other_form(self, obj, data):
        other_form = OtherForm(
            location=obj,
            usage_form=data['usage_form'],
            litteral_year=data['litteral_year'],
            year=data['year'],
            book=Book.objects.get(pk=data['book']),
            reference=data['reference']
        )
        other_form.save()

    def add_attested_form(self, obj, data):
        attested_form = AttestedForm(
            location=obj,
            attested_form=data['attested_form'],
            is_labeled=data['is_labeled'] == 'true',
            litteral_year=data['litteral_year'],
            year=data['year'],
            book=Book.objects.get(pk=data['book']),
            reference=data['reference']
        )
        attested_form.save()

    def update_standardized_form(self, obj, data):
        obj = StandardizedForm.objects.get(pk=data['id'])
        obj.standardized_form = data['standardized_form']
        obj.date = data['date']
        obj.save()

    def update_phonetic_transcription(self, obj, data):
        obj = PhoneticTranscription.objects.get(pk=data['id'])
        obj.phonetic_transcription = data['phonetic_transcription']
        obj.is_standard = data['is_standard'] == 'on'
        obj.informant = Informant.objects.get(pk=data['informant']) if data['informant'] else None
        obj.created_at = data['created_at']
        obj.save()

    def update_old_form(self, obj, data):
        obj = OldForm.objects.get(pk=data['id'])
        obj.old_form = data['old_form']
        obj.litteral_year = data['litteral_year']
        obj.year = data['year']
        obj.book = Book.objects.get(pk=data['book']) if data['book'] else None
        obj.reference = data['reference']
        obj.save()

    def update_other_form(self, obj, data):
        obj = OtherForm.objects.get(pk=data['id'])
        obj.usage_form = data['usage_form']
        obj.litteral_year = data['litteral_year']
        obj.year = data['year']
        obj.book = Book.objects.get(pk=data['book']) if data['book'] else None
        obj.reference = data['reference']
        obj.save()

    def update_attested_form(self, obj, data):
        obj = AttestedForm.objects.get(pk=data['id'])
        obj.attested_form = data['attested_form']
        obj.is_labeled = data['is_labeled'] == 'on'
        obj.litteral_year = data['litteral_year']
        obj.year = data['year']
        obj.book = Book.objects.get(pk=data['book']) if data['book'] else None
        obj.reference = data['reference']
        obj.save()

    def delete_standardized_form(self, obj, data):
        StandardizedForm.objects.get(location=obj, pk=data['id']).delete()

    def delete_phonetic_transcription(self, obj, data):
        PhoneticTranscription.objects.get(location=obj, pk=data['id']).delete()

    def delete_old_form(self, obj, data):
        OldForm.objects.get(location=obj, pk=data['id']).delete()

    def delete_other_form(self, obj, data):
        OtherForm.objects.get(location=obj, pk=data['id']).delete()

    def delete_attested_form(self, obj, data):
        AttestedForm.objects.get(location=obj, pk=data['id']).delete()


class SkridaozerKerofisTemplateView(View):

    def get(self, request, *args, **kwargs):
        template = 'semantic/skridaozer/kerofis/partial/'
        context = {
            'informants': Informant.objects.all().order_by('first_name', 'last_name'),
            'books_old': Book.objects.filter(is_kerofis_old=True).order_by('abbrevation'),
            'books': Book.objects.all().order_by('abbrevation')
        }
        if self.kwargs['template'] == 'standardized_form':
            template += 'standardized_form.html'
            context['obj'] = StandardizedForm.objects.get(pk=self.kwargs['id'])
        elif self.kwargs['template'] == 'phonetic_transcription':
            template += 'phonetic_transcription.html'
            context['obj'] = PhoneticTranscription.objects.get(pk=self.kwargs['id'])
        elif self.kwargs['template'] == 'old_form':
            template += 'old_form.html'
            context['obj'] = OldForm.objects.get(pk=self.kwargs['id'])
        elif self.kwargs['template'] == 'other_form':
            template += 'other_form.html'
            context['obj'] = OtherForm.objects.get(pk=self.kwargs['id'])
        elif self.kwargs['template'] == 'attested_form':
            template += 'attested_form.html'
            context['obj'] = AttestedForm.objects.get(pk=self.kwargs['id'])
        else:
            raise NotImplemented
        return render(request, template, context=context)
