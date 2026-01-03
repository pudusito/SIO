from django import forms
from ..models.profesional import Profesional
from core.validators import validar_rut

class ProfesionalForm(forms.ModelForm):
    """
    Formulario para la creación y edición de Profesionales.
    Incluye validaciones de formato (RUT, Correo) y estilizado CSS.
    """

    class Meta:
        model = Profesional
        fields = [
            'rut', 'tipo', 'nombre', 'primer_apellido', 'segundo_apellido',
            'telefono', 'correo', 'activo'
        ]
        
        # --- WIDGETS Y CLASES CSS ---
        # Aquí inyectamos el estilo 'Finexy' directamente al input
        widgets = {
            'rut': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Ej: 12.345.678-9 (Sin puntos también sirve)',
                'autocomplete': 'off'
            }),
            'tipo': forms.Select(attrs={
                'class': 'form-select'
            }),
            'nombre': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Nombres completos'
            }),
            'primer_apellido': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Primer apellido'
            }),
            'segundo_apellido': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Segundo apellido (Opcional)'
            }),
            'telefono': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': '+56 9 1234 5678'
            }),
            'correo': forms.EmailInput(attrs={
                'class': 'form-input',
                'placeholder': 'ejemplo@hospital.cl'
            }),
            'activo': forms.CheckboxInput(attrs={
                'class': 'form-checkbox',
                # 'checked': True # Opcional: si quieres que venga marcado por defecto
            }),
        }

        # --- TEXTOS DE AYUDA ---
        help_texts = {
            'rut': 'Ingrese el RUT con o sin puntos, con guión y dígito verificador.',
            'tipo': 'Seleccione el rol clínico que desempeñará en pabellón.',
            'activo': 'Desmarcar solo si el profesional ya no trabaja en el servicio.'
        }

        # --- ETIQUETAS PERSONALIZADAS ---
        labels = {
            'rut': 'RUT / Run',
            'tipo': 'Cargo / Rol',
            'telefono': 'Teléfono de Contacto',
            'activo': '¿Profesional Activo?'
        }

    # --- VALIDACIONES PERSONALIZADAS (CLEAN METHODS) ---

    def clean_rut(self):
        """
        Normaliza el RUT: Lo convierte a mayúsculas y quita espacios extra.
        """
        rut = self.cleaned_data.get('rut')
        if rut: 
            verificacion_rut = validar_rut(rut)
            if not verificacion_rut[0]:
                raise forms.ValidationError(verificacion_rut[1])
        return rut


    def clean_correo(self):
        """
        Valida que el correo sea único (excepto si es el mismo usuario editándose).
        """
        correo = self.cleaned_data.get('correo')
        if correo:
            # Buscamos si existe otro profesional con este correo
            existe = Profesional.objects.filter(correo=correo).exclude(pk=self.instance.pk).exists()
            if existe:
                raise forms.ValidationError("Este correo electrónico ya está registrado por otro profesional.")
        return correo

    def clean(self):
        """
        Validaciones cruzadas globales (si fueran necesarias).
        Por ahora está limpio, pero aquí podrías validar lógica compleja como en PartoForm.
        """
        cleaned_data = super().clean()
        return cleaned_data