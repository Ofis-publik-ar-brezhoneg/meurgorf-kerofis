import uuid
import base64

from django.core.files.base import ContentFile
from django.db.models import Max

from rest_framework import serializers

from .models import DerivedForm
from .models import GrammaticalCategory
from .models import HistoricalOccurrence
from .models import Term
from .models import Variant
from .models import PhoneticForm
from commun.serializers import BookSerializer


class GrammaticalCategorySerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()
    abbreviation = serializers.SerializerMethodField()

    class Meta:
        model = GrammaticalCategory
        fields = ('id', 'title', 'abbreviation')

    def get_title(self, obj):
        lang = self.context['request'].headers.get('Accept-Language', 'fr_FR')
        return obj.title_bre if lang != 'fr_FR' else obj.title_fra

    def get_abbreviation(self, obj):
        lang = self.context['request'].headers.get('Accept-Language', 'fr_FR')
        return obj.abbreviation_bre if lang != 'fr_FR' else obj.abbreviation_fra
    
    def to_internal_value(self, data):
        if 'id' in data.keys():
            return GrammaticalCategory.objects.get(pk=data['id'])
        return super(GrammaticalCategorySerializer, self).to_internal_value(data)


class DerivedFormSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = DerivedForm
        fields = ('id', 'form', 'order', 'sub_order')


class VariantSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = Variant
        fields = ('id', 'variant')


class HistoricalOccurrenceSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    book = BookSerializer()

    class Meta:
        model = HistoricalOccurrence
        fields = ('id', 'occurence', 'occurence_normalized', 'litteral_year', 'year', 'book', 'reference')


class ParentTermSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    grammatical_category = GrammaticalCategorySerializer()

    class Meta:
        model = Term
        fields = ('id', 'canonic_form', 'grammatical_category')
        read_only_fields = ('canonic_form', 'grammatical_category')


class PhoneticFormSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    link = serializers.CharField(required=False)

    class Meta:
        model = PhoneticForm
        fields = ('id', 'phonetic_form', 'phonetic_file', 'link')


class TermSerializer(serializers.ModelSerializer):
    grammatical_category = GrammaticalCategorySerializer()
    derived_forms = DerivedFormSerializer(many=True, required=False)
    variants = VariantSerializer(many=True, required=False)
    historical_occurrences = HistoricalOccurrenceSerializer(many=True, required=False)
    parents = ParentTermSerializer(many=True, required=False)
    phonetic_forms = PhoneticFormSerializer(many=True, required=False)

    class Meta:
        model = Term
        fields = ('id', 'canonic_form', 'grammatical_category', 'usage', 'derived_forms', 'historical_occurrences',
                  'definition', 'parents', 'variants', 'study_notes', 'etymology', 'phonetic_forms')

    def update(self, instance, validated_data):
        for variant in validated_data.pop("variants", []):
            if variant.get('id'):
                new_variant = Variant.objects.get(pk=variant['id'])
                new_variant.variant = variant['variant']
            else:
                new_variant = Variant(variant=variant['variant'])

            new_variant.save()
            instance.variants.add(new_variant)

        for derived_form in validated_data.pop("derived_forms", []):
            if derived_form.get('id'):
                new_derived_form = DerivedForm.objects.get(pk=derived_form['id'])
                new_derived_form.form = derived_form['form']
                if 'order' in derived_form.keys():
                    new_derived_form.order = derived_form['order']
            else:
                max_order = DerivedForm.objects.filter(term=instance).aggregate(Max('order')).get('order__max') or 0
                new_derived_form = DerivedForm(form=derived_form['form'], order=max_order + 1)

            new_derived_form.save()
            instance.derived_forms.add(new_derived_form)

        for historical_occurrence in validated_data.pop("historical_occurrences", []):
            if historical_occurrence.get('id'):
                new_historical_occurrence = HistoricalOccurrence.objects.get(pk=historical_occurrence['id'])
                new_historical_occurrence.occurence = historical_occurrence['occurence']
                new_historical_occurrence.litteral_year = historical_occurrence['litteral_year']
                new_historical_occurrence.year = historical_occurrence['year']
                new_historical_occurrence.book = historical_occurrence['book']
                new_historical_occurrence.reference = historical_occurrence['reference']
            else:
                new_historical_occurrence = HistoricalOccurrence()
                new_historical_occurrence.occurence = historical_occurrence['occurence']
                new_historical_occurrence.litteral_year = historical_occurrence['litteral_year']
                new_historical_occurrence.year = historical_occurrence['year']
                new_historical_occurrence.book = historical_occurrence['book']
                new_historical_occurrence.reference = historical_occurrence['reference']

            new_historical_occurrence.save()
            instance.historical_occurrences.add(new_historical_occurrence)

        if 'parents' in validated_data.keys() and not validated_data['parents']:
            instance.parents.clear()

        parents_id = set([parent['id'] for parent in validated_data.pop("parents", [])])
        if parents_id:
            instance.parents.set([Term.objects.get(pk=parent_id) for parent_id in parents_id])

        for phonetic_form in validated_data.pop("phonetic_forms", []):
            if phonetic_form.get('id'):
                new_phonetic_form = PhoneticForm.objects.get(pk=phonetic_form['id'])
            else:
                new_phonetic_form = PhoneticForm()
            new_phonetic_form.phonetic_form = phonetic_form['phonetic_form']

            if phonetic_form.get('link'):
                format, imgstr = phonetic_form.get('link').split(';base64,')
                ext = format.split('/')[-1]

                link = ContentFile(base64.b64decode(imgstr), name=f"{uuid.uuid4()} {ext}")
                new_phonetic_form.phonetic_file = link
            new_phonetic_form.save()

            instance.phonetic_forms.add(new_phonetic_form)

        return super(TermSerializer, self).update(instance, validated_data)


class GrammaticalCategoryStatSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()
    abbreviation = serializers.SerializerMethodField()
    terms_count = serializers.SerializerMethodField()

    class Meta:
        model = GrammaticalCategory
        fields = ('title', 'abbreviation', 'terms_count')

    def get_title(self, obj):
        lang = self.context['request'].headers.get('Accept-Language', 'fr_FR')
        return obj.title_bre if lang != 'fr_FR' else obj.title_fra

    def get_abbreviation(self, obj):
        lang = self.context['request'].headers.get('Accept-Language', 'fr_FR')
        return obj.abbreviation_bre if lang != 'fr_FR' else obj.abbreviation_fra

    def get_terms_count(self, obj):
        return obj.terms.count()
