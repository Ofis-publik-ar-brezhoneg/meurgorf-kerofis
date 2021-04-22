from django.forms import ModelForm
from .models import Term


class TermForm(ModelForm):
    class Meta:
        model = Term
        exclude = ['created_at', 'created_by', 'old_id', 'parents']
