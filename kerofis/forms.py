from django.forms import ModelForm
from .models import Location


class LocationForm(ModelForm):
    class Meta:
        model = Location
        exclude = ['created_at', 'created_by', 'old_id']
