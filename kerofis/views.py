from django.core.paginator import Paginator
from django.views.generic import TemplateView
from django.views.generic import RedirectView
from django.urls import reverse

from .models import Category
from .models import City
from .models import Department
from .models import Location

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
