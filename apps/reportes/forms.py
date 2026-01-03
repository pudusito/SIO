# form for confirm date range 
from django import forms
from django.utils import timezone


class RangeDateReportForm(forms.Form):
    start_date = forms.DateField(widget=forms.DateInput(attrs={
        'type': 'date'
    }), required=True)

    end_date = forms.DateField(widget=forms.DateInput(attrs={
        'type': 'date'
    }), required=True)



    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')


        return cleaned_data