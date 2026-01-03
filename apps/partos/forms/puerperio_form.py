from django import forms
from ..models import Puerperio


class PuerperioForm(forms.ModelForm):
    class Meta:
        model = Puerperio
        exclude = ['created_by', 'updated_by', 'parto']
        