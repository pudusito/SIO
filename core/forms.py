from django import forms



class MotivoForm(forms.Form):
    # minimo 15 caracteres
    motivo = forms.CharField(min_length=15, max_length=150, widget=forms.Textarea(
        attrs={
            "placeholder": "Justifique el Motivo de la accion que pretende realizar"
        }
    ), required=True)