from django.contrib.auth.models import User

from rest_framework import serializers

from .models import Book


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'groups', 'is_staff', 'is_superuser')


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'


class DynamicSerializer(serializers.Serializer):
    class Meta:
        fields = ('', )

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass

    def __init__(self, *args, dyn_fields=None, **kwargs):
        dyn_fields = dyn_fields or []
        for field in dyn_fields:
            self.fields[field] = serializers.CharField()

        super().__init__(self, *args, **kwargs)
