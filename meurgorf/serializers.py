from rest_framework import serializers

from .models import GrammaticalCategory
from .models import Term


class GrammaticalCategoryStatSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()
    abbreviation = serializers.SerializerMethodField()
    terms_count = serializers.SerializerMethodField()
    percent = serializers.SerializerMethodField()

    class Meta:
        model = GrammaticalCategory
        fields = ('title', 'abbreviation', 'terms_count', 'percent')

    def get_title(self, obj):
        lang = self.context['request'].headers.get('Accept-Language', 'fr_FR')
        return obj.title_bre if lang != 'fr_FR' else obj.title_fra

    def get_abbreviation(self, obj):
        lang = self.context['request'].headers.get('Accept-Language', 'fr_FR')
        return obj.abbreviation_bre if lang != 'fr_FR' else obj.abbreviation_fra

    def get_terms_count(self, obj):
        return obj.terms.count()

    def get_percent(self, obj):
        return round((obj.terms.count() / Term.objects.count()) * 100, 2)
