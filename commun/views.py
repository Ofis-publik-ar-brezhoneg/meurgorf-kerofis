from django.contrib.auth.models import User
from django.db.models import Q
from django.views.generic import TemplateView

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.views import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.viewsets import GenericViewSet

from .filters import BookFilter
from .models import Book
from .serializers import UserSerializer
from .serializers import BookSerializer
from .inspect import get_all_fields_info


class UsersView(ModelViewSet):
    serializer_class = UserSerializer
    model = User
    queryset = User.objects.all()

    @action(methods=['get'], detail=False)
    def me(self, request, pk=None):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)


class BooksView(ModelViewSet):
    serializer_class = BookSerializer
    model = Book
    queryset = Book.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_class = BookFilter


class OldExportView(GenericViewSet):
    def list(self, request, *args, **kwargs):
        return Response(get_all_fields_info(self.model, ignore_relations=[self.model]))

    @staticmethod
    def _filters(operations):
        operators = {
            '=': '',
            '>': 'gt',
            '<': 'lt'
        }
        operations_index = set(map(lambda x: int(x[x.find('_') + 1:]), operations))
        for index in operations_index:
            field = operations[f"field_{index}"]
            operator = operators.get(operations[f"operator_{index}"])
            if operator:
                field += f"__{operator}"
            value = operations[f"value_{index}"]

            yield Q(**{field: value})

    @staticmethod
    def _order_by(orders):
        return ('id', )

    @action(methods=['post'], detail=False)
    def export(self, request, pk=None):
        fields = request.data['fields']['fields']
        operations = request.data['operations']
        orders = request.data['orders']
        queryset = self.get_queryset().filter(*self._filters(operations)).order_by(*self._order_by(orders))

        return Response(queryset.values_list(*fields, named=True))


###


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

            print(field, value)

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
