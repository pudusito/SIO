from django import forms
from dal import autocomplete
from ..models import Gestacion


class GestacionForm(forms.ModelForm):
    motivo = forms.CharField(max_length=200, widget=forms.Textarea(attrs={
        "placeholder": "Ingrese el motivo de la actualizacion"
    }), required=False)
    
    class Meta:
        model = Gestacion
        exclude = ['created_by', 
                   'created_at', 
                   'updated_by', 
                   'updated_at', 
                   'fecha_inicio_gestacion']
        widgets = {
            'fur': forms.DateInput(attrs={
                "type": "date"
            }),
            'fecha_eco': forms.DateInput(attrs={
                "type": "date"
            }),
            'numero_fetos': forms.NumberInput(attrs={
                "placeholder": "Ingrese el número de fetos"
            }),
            'semanas_eco': forms.NumberInput(attrs={
                "placeholder": "0"
            }),
            'dias_eco': forms.NumberInput(attrs={
                "placeholder": "0"
            }),
            'paciente': autocomplete.ModelSelect2(url='gestacion:autocompletar_paciente', attrs={
                "class ": "autocompletado",
                'data-placeholder': "Busque por nombre o por Rut/Identificacion"
            })
        }

        
        help_texts = {
            'paciente': "Puede buscar por Rut o Nombre completo del paciente",
            'numero_fetos': "Si ingresa mas de uno, recuerde marcar multiple",
            'origen_datacion': "El origen seleccionado es el que tomara el sistema para calcular la semanas de gestación"

        }




    def clean_motivo(self):
        motivo = self.cleaned_data.get('motivo')
        if self.instance.pk and not motivo:
            raise forms.ValidationError("Debe especificar el motivo de la actualizacion")
        return motivo
    


    def clean(self):
        cleaned_data = super().clean()
        multiple = cleaned_data.get('multiple')
        n_fetos = cleaned_data.get('numero_fetos')

        # Datos asociados a como se obtuvieron las semanas de gestacion
        origen_datacion = cleaned_data.get('origen_datacion')
        fur = cleaned_data.get('fur')
        fecha_eco = cleaned_data.get('fecha_eco')
        semanas_eco = cleaned_data.get('semanas_eco')
        dias_eco = cleaned_data.get('dias_eco')

        # Riesgo
        diabetes = cleaned_data.get('diabetes')
        hipertesion = cleaned_data.get('hipertension')
        enfermedad_cardiaca = cleaned_data.get('enfermedad_cardiaca')
        riesgo = cleaned_data.get('riesgo')

        if (diabetes or hipertesion or enfermedad_cardiaca) and riesgo == "bajo":
            self.add_error("riesgo", "El riesgo no puede ser bajo si se ha marcado un factor de riesgo")


        if n_fetos is not None:
            if multiple and n_fetos <= 1:
                self.add_error('numero_fetos', 'Si es multiple la gestacion el número de fetos no puede ser menor o igual a 1')
            elif not multiple and n_fetos > 1:
                self.add_error('numero_fetos',  'No puede poner mas de un feto si no marca la gestacion como multiple')
        
        
        
        if origen_datacion == 'sin':
            if semanas_eco or dias_eco or fecha_eco or fur:
                self.add_error('origen_datacion', 'Si no marca el origen de la datacion no puede especificar "FECHA DEL FUR", "SEMANAS ECO", "DIAS ECO" ')
                if semanas_eco:
                    self.add_error('semanas_eco', 'No puede especificar un valor')
                if fur:
                    self.add_error('fur', 'No puede especificar fecha FUR')
                if fecha_eco:
                    self.add_error('fecha_eco', 'No puede especificar fecha eco')

                if dias_eco:
                    self.add_error('dias_eco', 'No puede especificar dias eco')
            
        elif origen_datacion == 'fur':
            if not fur:
                self.add_error('fur', "Si datacion es FUR debe especificar la fecha del FUR")
        elif origen_datacion == 'eco':
            if not semanas_eco:
                self.add_error('semanas_eco', 'Si datacion es ECO debe especificar el numero de semanas')
            if not dias_eco:
                self.add_error('dias_eco', 'Si datacion es ECO debe especificar el numero de dias')
            if not fecha_eco:
                self.add_error('fecha_eco', 'Si datacion es ECO debe especificar la fecha de ecografia')
        return cleaned_data
            
        