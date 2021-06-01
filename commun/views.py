from contextlib import suppress

from django.db.models import Q
from django.views.generic import TemplateView
from django.views.generic import RedirectView

from .models import Book
from .inspect import get_all_fields_info


class SkridaozerBookView(TemplateView):
    template_name = 'semantic/skridaozer/mammennoù.html'

    def post(self, request, *args, **kwargs):
        data = self.request.POST

        instance = Book.objects.get(pk=self.kwargs['book_id'])
        instance.abbrevation = data['abbrevation']
        instance.title = data['title']
        instance.description = data['description']
        instance.author = data['author']
        instance.is_kerofis_old = data.get('is_kerofis_old', False) == 'on'
        instance.is_kerofis_other = data.get('is_kerofis_other', False) == 'on'
        instance.is_kerofis_attested = data.get('is_kerofis_attested', False) == 'on'
        instance.is_meurgorf = data.get('is_meurgorf', False) == 'on'
        instance.is_active = data.get('is_active', False) == 'on'
        instance.save()

        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if kwargs.get('book_id'):
            context['book'] = Book.objects.get(pk=self.kwargs['book_id'])
        if self.request.GET.get('abbrevation') or self.request.GET.get('title'):
            context['books'] = Book.objects.filter(abbrevation__icontains=self.request.GET.get('abbrevation'),
                                                   title__icontains=self.request.GET.get('title'))
        else:
            context['books'] = Book.objects.all()

        return context


class SkridaozerDeleteBookView(RedirectView):
    pattern_name = 'skridaozer:mammennou'

    def get_redirect_url(self, *args, **kwargs):
        with suppress(Book.DoesNotExist):
            Book.objects.get(pk=self.kwargs.get('book_id')).delete()
        return super().get_redirect_url()


class SkridaozerAddBookView(RedirectView):
    pattern_name = 'skridaozer:mammennou'

    def get_redirect_url(self, *args, **kwargs):
        book = Book(abbrevation=self.request.GET.get('abbrevation'))
        book.save()
        return super().get_redirect_url(book_id=book.id)


class ExportView(TemplateView):
    template_name = 'semantic/skridaozer/commun/ezporzhian.html'
    model = None
    ignore_relations = []

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['fields'] = get_all_fields_info(self.model, ignore_relations=[self.model])

        return context

    @staticmethod
    def _filters(operations):
        operations_index = set(map(lambda x: int(x[x.find('_') + 1:]), operations))
        for index in operations_index:
            field = operations[f"field_{index}"]
            if operations[f"operator_{index}"] != '=':
                field += f"__{operations[f'operator_{index}']}"
            value = operations[f"value_{index}"]

            yield Q(**{field: value})

    @staticmethod
    def _order_by(orders):
        return ('id',)

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)

        operations = {}
        orders = {}
        fields = self.request.POST.getlist('fields')
        for name in self.request.POST.keys():
            if name[:10] == 'operation_':
                operations[name[10:]] = self.request.POST[name]
            if name[:6] == 'order_':
                orders[name[:6]] = self.request.POST[name]

        queryset = self.model.objects.filter(*self._filters(operations)).order_by(*self._order_by(orders))
        context['data'] = queryset.values_list(*fields, named=True)
        context['selected_fields'] = fields
        context['operations'] = operations
        context['orders'] = orders

        return self.render_to_response(context)
