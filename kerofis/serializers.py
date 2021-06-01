import uuid
import base64

from django.core.files.base import ContentFile

from rest_framework import serializers

from .models import Location
from .models import Category
from .models import City
from .models import Department
from .models import StandardizedForm
from .models import PhoneticTranscription
from .models import OtherForm
from .models import AttestedForm
from .models import OldForm
from .models import PhoneticTranscriptionLink


class LocationCategorySerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ('id', 'name')

    def get_name(self, obj):
        lang = self.context['request'].headers.get('Accept-Language', 'fr_FR')
        return obj.name_bre if lang != 'fr_FR' else obj.name_fra

    def to_internal_value(self, data):
        if 'id' in data.keys():
            return Category.objects.get(pk=data['id'])
        return super(LocationCategorySerializer, self).to_internal_value(data)


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'


class CitySerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    department = DepartmentSerializer()

    class Meta:
        model = City
        fields = '__all__'


class StandardizedFormSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = StandardizedForm
        fields = ('id', 'standardized_form', 'date')


class PhoneticTranscriptionLinksSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhoneticTranscriptionLink
        fields = '__all__'


class PhoneticTranscriptionsSerializer(serializers.ModelSerializer):
    informant = serializers.SerializerMethodField()
    links = PhoneticTranscriptionLinksSerializer(many=True, required=False)
    link = serializers.CharField(required=False)

    class Meta:
        model = PhoneticTranscription
        fields = ('id', 'phonetic_transcription', 'is_standard', 'created_at', 'informant', 'links', 'link')

    def get_informant(self, instance):
        return f"{instance.informant.first_name} {instance.informant.last_name}" if instance.informant else ''


class OtherFormsSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = OtherForm
        fields = '__all__'


class AttestedFormSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = AttestedForm
        fields = '__all__'


class OldFormsSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = OldForm
        fields = '__all__'


class LocationSerializer(serializers.ModelSerializer):
    category = LocationCategorySerializer()
    city = CitySerializer()
    department = DepartmentSerializer()
    standardized_forms = StandardizedFormSerializer(many=True, required=False)
    phonetic_transcriptions = PhoneticTranscriptionsSerializer(many=True, required=False)
    phonetic_transcriptions_list = serializers.SerializerMethodField(required=False)
    other_forms = OtherFormsSerializer(many=True, required=False)
    attested_forms = AttestedFormSerializer(many=True, required=False)
    old_forms = OldFormsSerializer(many=True, required=False)
    postal_code = serializers.CharField(required=False)
    insee_code = serializers.CharField(required=False)

    class Meta:
        model = Location
        fields = ('id', 'category', 'city', 'department', 'standardized_forms', 'phonetic_transcriptions',
                  'phonetic_transcriptions_list', 'other_forms', 'attested_forms', 'name', 'on_ign', 'ign_date',
                  'formalized_date', 'is_public', 'generic_name', 'on_bf', 'reference', 'notes', 'formalized_proposal',
                  'proposal_author', 'square_bf', 'longitude', 'latitude', 'etymological_note_bre', 'old_forms',
                  'etymological_note_fra', 'created_at', 'created_by', 'postal_code',
                  'insee_code')

    def get_phonetic_transcriptions_list(self, instance):
        return [obj.phonetic_transcription for obj in instance.phonetic_transcriptions.all()]

    def update(self, instance, validated_data):
        for standardized_form in validated_data.pop("standardized_forms", []):
            if standardized_form.get('id'):
                new_standardized_form = StandardizedForm.objects.get(pk=standardized_form['id'])
                new_standardized_form.standardized_form = StandardizedForm['standardized_form']
                new_standardized_form.date = StandardizedForm['date']
            else:
                new_standardized_form = StandardizedForm(
                    standardized_form=standardized_form['standardized_form'],
                    date=standardized_form['date'])

            new_standardized_form.save()
            instance.standardized_forms.add(new_standardized_form)

        for phonetic_transcription in validated_data.pop("phonetic_transcriptions", []):
            if phonetic_transcription.get('id'):
                new_phonetic_transcription = PhoneticTranscription.objects.get(pk=phonetic_transcription['id'])
            else:
                new_phonetic_transcription = PhoneticTranscription()
            new_phonetic_transcription.phonetic_transcription = phonetic_transcription['phonetic_transcription']
            new_phonetic_transcription.is_standard = phonetic_transcription['is_standard']
            new_phonetic_transcription.informant = phonetic_transcription.get('informant')
            new_phonetic_transcription.created_at = phonetic_transcription['created_at']
            new_phonetic_transcription.save()

            if phonetic_transcription.get('link'):
                format, imgstr = phonetic_transcription.get('link').split(';base64,')
                ext = format.split('/')[-1]

                link = ContentFile(base64.b64decode(imgstr), name=f"{uuid.uuid4()} {ext}")
                new_phonetic_link = PhoneticTranscriptionLink()
                new_phonetic_link.link = link
                new_phonetic_link.phonetic_transcription = new_phonetic_transcription
                new_phonetic_link.save()

            instance.phonetic_transcriptions.add(new_phonetic_transcription)

        for old_form in validated_data.pop("old_forms", []):
            if old_form.get('id'):
                new_old_form = OldForm.objects.get(pk=old_form['id'])
            else:
                new_old_form = OldForm()
            new_old_form.old_form = old_form['old_form']
            new_old_form.litteral_year = old_form['litteral_year']
            new_old_form.year = old_form['year']
            new_old_form.book = old_form['book']
            new_old_form.reference = old_form['reference']
            new_old_form.save()
            instance.old_forms.add(new_old_form)

        for other_form in validated_data.pop("other_forms", []):
            if other_form.get('id'):
                new_other_form = OtherForm.objects.get(pk=other_form['id'])
            else:
                new_other_form = OtherForm()
            new_other_form.usage_form = other_form['usage_form']
            new_other_form.litteral_year = other_form['litteral_year']
            new_other_form.book = other_form['book']
            new_other_form.reference = other_form['reference']
            new_other_form.save()
            instance.other_forms.add(new_other_form)

        for attested_form in validated_data.pop("attested_forms", []):
            if attested_form.get('id'):
                new_attested_form = AttestedForm.objects.get(pk=attested_form['id'])
            else:
                new_attested_form = AttestedForm()
            new_attested_form.attested_form = attested_form['attested_form']
            new_attested_form.is_labeled = attested_form['is_labeled']
            new_attested_form.litteral_year = attested_form['litteral_year']
            new_attested_form.book = attested_form['book']
            new_attested_form.reference = attested_form['reference']
            new_attested_form.save()
            instance.attested_forms.add(new_attested_form)

        city = validated_data.pop("city", None)
        insee_code = validated_data.pop("insee_code", None)
        postal_code = validated_data.pop("postal_code", None)
        if city:
            instance.city = City.objects.get(pk=city['id'])
        if insee_code:
            instance.city.insee_code = insee_code
        if postal_code:
            instance.city.postal_code = postal_code
        if insee_code or postal_code:
            instance.city.save()

        return super().update(instance, validated_data)


class CategoryStatSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    locations_count = serializers.SerializerMethodField()
    percent = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ('name', 'locations_count', 'percent')

    def get_name(self, obj):
        lang = self.context['request'].headers.get('Accept-Language', 'fr_FR')
        return obj.name_bre if lang != 'fr_FR' else obj.name_fra

    def get_locations_count(self, obj):
        return obj.locations.count()

    def get_percent(self, obj):
        return round((obj.locations.count() / Location.objects.count()) * 100, 2)
