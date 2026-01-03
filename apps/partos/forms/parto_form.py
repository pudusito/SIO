from django import forms
from django.utils import timezone
from dal import autocomplete

from ..models import Parto


class PartoForm(forms.ModelForm):
    motivo = forms.CharField(max_length=200, widget=forms.Textarea(attrs={
        "placeholder": "Ingrese el motivo de la actualizacion"
    }), required=False)


    # Sobreescribir el field por defecto que usa un form para los datetimefield de los modelos
    # en django, este permite un datetimefield del modelo dividirlo en 2 field input html diferentes
    # pero que luego se unen como un solo datetime para ser almacenado en el modelo
    hora_inicio = forms.SplitDateTimeField(
        input_date_formats=['%Y-%m-%d'],
        input_time_formats=['%H:%M:%S', '%H:%M'], # Aquí la flexibilidad
        widget=forms.SplitDateTimeWidget(
            date_attrs={"type": "date"},
            time_attrs={"type": "time"}
        )
    )
    tiempo_membrana_rota = forms.IntegerField(min_value=0, widget=forms.NumberInput(attrs={
        'placeholder': 'En minutos'
    }), help_text="Tiempo en minutos", required=True)

    tiempo_dilatacion = forms.IntegerField(min_value=0, widget=forms.NumberInput(attrs={
        'placeholder': 'En minutos'
    }), help_text="Tiempo en minutos", required=True)

    tiempo_expulsivo = forms.IntegerField(min_value=0, widget=forms.NumberInput(attrs={
        'placeholder': 'En minutos'
    }), help_text="Tiempo en minutos", required=True)


    class Meta:
        model = Parto
        exclude = [
            'created_by', 'created_at', 'updated_by', 'updated_at',
            'edad_madre'
            ]
        widgets = {
            'complicaciones': forms.CheckboxSelectMultiple(),
            'hora_inicio': forms.SplitDateTimeWidget(
                # Estos son argumentos válidos para el SplitDateTimeWidget:
                date_format='%Y-%m-%d', 
                time_format=['%H:%M:%S', '%H:%M'],                
                date_attrs={"type": "date"},
                time_attrs={"type": "time"}
                
            ),
            'observaciones': forms.Textarea(attrs={
                "placeholder": "Ingrese observaciones sobre el trabajo de parto si las hay, si no puede dejar en blanco"
            }),
            'gestacion': autocomplete.ModelSelect2(url='parto:autocompletar_gestacion', attrs={
                "class": "autocompletado",
                "data-placeholder": "Busque por Identificacion/Nombre/CodigoGestacion"
            })
            }

        help_texts = {
            'gestacion': 'Puede buscarla por Nombre Completo del Paciente, Identificación o Código de la Gestación',
            'hora_inicio': 'Proporcione la fecha y hora cuando inicio el parto. No al momento de registrarlo.',
            'grupo_robson': "Marque un grupo robson solo si la via de nacimiento es Cesarea"
        }


    def clean_motivo(self):
        motivo = self.cleaned_data.get('motivo')
        if self.instance.pk and not motivo:
            raise forms.ValidationError("Debe especificar el motivo de la actualizacion")
        return motivo


    def clean_tiempo_membrana_rota(self):
        tiempo_membrana_rota = self.cleaned_data.get('tiempo_membrana_rota')
        tiempo_membrana_rota = timezone.timedelta(minutes=tiempo_membrana_rota)
        return tiempo_membrana_rota

    
    def clean_tiempo_dilatacion(self):
        tiempo_dilatacion = self.cleaned_data.get('tiempo_dilatacion')
        tiempo_dilatacion = timezone.timedelta(minutes=tiempo_dilatacion)
        return tiempo_dilatacion
    

    def clean_tiempo_expulsivo(self):
        tiempo_expulsivo = self.cleaned_data.get('tiempo_expulsivo')
        tiempo_expulsivo = timezone.timedelta(minutes=tiempo_expulsivo)
        return tiempo_expulsivo
    
    def clean(self):
        cleaned_data =  super().clean()
        via_nacimiento = cleaned_data.get('via_nacimiento')
        grupo_robson = cleaned_data.get('grupo_robson')
        print(cleaned_data.get("hora_inicio"))
        if via_nacimiento:
            if (via_nacimiento.tipo == "CES.ELECTIVA" or via_nacimiento.tipo == "CES. URGENCIA") and not (grupo_robson):
                self.add_error('grupo_robson', 'Si la via de nacimiento es por cesarea debe añadir grupo robson')
            elif (via_nacimiento.tipo == "EUTOCICO" or via_nacimiento.tipo == "DISTOCICO") and grupo_robson:
                self.add_error('grupo_robson', 'El grupo robson solo debe estar marcado en los partos por cesarea')
        return cleaned_data