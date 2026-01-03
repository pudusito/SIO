from django import forms
from django.utils import timezone
from ..models import TestSgb, TestHepatitisB, TestVdrl, TestVih



class AbstractTestForm(forms.ModelForm):
    class Meta:
        exclude=['created_at', 'orden']
        widgets = {
            'fecha_toma': forms.DateInput(attrs={'type':'date'})
        }


    def clean_fecha_toma(self):
        fecha_toma = self.cleaned_data.get('fecha_toma')
        fecha_actual = timezone.now().date()
        if fecha_actual < fecha_toma:
            raise forms.ValidationError('La fecha que se toma al examen no puede ser antes que la de HOY')
        return fecha_actual
    

class TestSgbForm(AbstractTestForm):
    class Meta(AbstractTestForm.Meta):
        model = TestSgb


class TestVihForm(AbstractTestForm):
    class Meta(AbstractTestForm.Meta):
        model = TestVih


class TestHepatitisBForm(AbstractTestForm):
    class Meta(AbstractTestForm.Meta):
        model = TestHepatitisB


class TestVdrlForm(AbstractTestForm):
    class Meta(AbstractTestForm.Meta):
        model = TestVdrl