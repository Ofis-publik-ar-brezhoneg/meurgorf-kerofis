from django.contrib.auth.models import User
from django.db.models import Q

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


class ExportView(GenericViewSet):
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
