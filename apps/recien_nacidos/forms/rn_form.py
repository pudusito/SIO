from django import forms
from dal import autocomplete


from ..models import RecienNacido


class RecienNacidoForm(forms.ModelForm):
    motivo = forms.CharField(max_length=200, widget=forms.Textarea(attrs={
        "placeholder": "Ingrese el motivo de la actualizacion"
    }), required=False)


    fecha_hora = forms.SplitDateTimeField( 
        input_date_formats=['%Y-%m-%d'],
        input_time_formats=['%H:%M:%S', '%H:%M'], # Aquí la flexibilidad
        widget=forms.SplitDateTimeWidget(
            date_attrs={"type": "date"},
            time_attrs={"type": "time"}
        )

    )


   

    class Meta:
        model = RecienNacido
        exclude = ['created_by', 'created_at', 'updated_by', 'updated_at']
        widgets = {
            'complicaciones_postparto': forms.CheckboxSelectMultiple(),
            'reanimaciones_neonatales': forms.CheckboxSelectMultiple(),
            'peso': forms.NumberInput(attrs={
            'placeholder': 'Ej: 1500'
            }),
            'talla': forms.NumberInput(attrs={
                'placeholder': 'Ej: 10'
            }),
            'parto': autocomplete.ModelSelect2(url="recien_nacido:autocompletar_parto", attrs={
                "class": "autocompletado",
                "data-placeholder": "Busque por Identificacion/Nombre/CodigoParto"
            })
        }



    def clean_motivo(self):
        motivo = self.cleaned_data.get('motivo')
        if self.instance.pk and not motivo:
            raise forms.ValidationError("Debe especificar el motivo de la actualizacion")
        return motivo


   # ACORDARSE AÑADIR LAS VALIDACIONES LUEGO
    def clean(self):
        cleaned_data = super().clean()
        apgar_1 = cleaned_data.get('apgar_1')
        reanimaciones = cleaned_data.get('reanimaciones_neonatales')
        destino = cleaned_data.get('destino')
        alojamiento = cleaned_data.get('alojamiento_conjunto')
        rn_fecha_hora = cleaned_data.get('fecha_hora')
        parto_instancia = cleaned_data.get('parto')
        apgar_5 = cleaned_data.get('apgar_5')

        # No tiene sentido que se marque alojamiento conjunto si esta en uci, uti o fallecido el RN
        if destino in ['uci', 'uti', 'fallecido'] and alojamiento:
            self.add_error('destino', 'El alojamiento conjunto no es posible si el destino es UCI, UTI, o Fallecimiento.')
        
        # apgar 1 no queda vacio y su valor es menor que 7 pero no tiene reanimaciones error pq deberia tener
        if apgar_1 is not None and apgar_1 < 7 and not reanimaciones:
            # Se lanza un error si la reanimación es requerida pero no marcada
            self.add_error('reanimaciones_neonatales', 'Apgar al minuto bajo (<7) indica necesidad de registrar reanimación.')

        # el bebe no puede haber nacido antes de la hora que inicio el trabajo de parto
        if rn_fecha_hora and parto_instancia:
            if rn_fecha_hora < parto_instancia.hora_inicio:
                self.add_error('fecha_hora', 'El RN no pudo haber nacido antes que empezara el trabajo de parto, revise la hora del parto o corriga la hora')

        # Validamos que el apgar 5 no sea menor que apgar 1
        if apgar_1 is not None and apgar_5 is not None and apgar_5 < apgar_1:
            self.add_error('apgar_5', 'El Apgar a los 5 minutos no puede ser inferior al Apgar al minuto.')

        if parto_instancia and parto_instancia.estado != "terminado":
            self.add_error('parto', 'No puede añadir recien nacidos a partos que aun no han terminado')

        return cleaned_data