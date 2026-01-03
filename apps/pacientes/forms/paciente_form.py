from django.utils import timezone
from django import forms
import phonenumbers

from ..models import Paciente
from core import utils, validators



'''
Apunte Daniel de mañana:
(Tenemos 2 formas para implementar los formularios de actualizacion y los que se incrustaran en otro)
1.Podemos facilmente a los formularios crear un campo llamado motivo que no sea obligatorio sea opcional total este valor lo manejaremos de forma 
independiente, que es el motivo de actualizacion podriamos crearcelo sin culpa a los usuarios y solo cargarloe en el template si es una actualizacion.
2.Pero si hacemos eso igual tendremos que crear un nuevo formulario que extienda del primero ya que en algunos formularios deberemos excluir un campo foreign key
ya que lo incrustaremos dentro de otro template el formulario que ya tiene la pk del objeto al cual lo asociaremos y en el formulario anterior no podemos dejar ese
valor como opcional.
'''


class PacienteForm(forms.ModelForm):   

    motivo = forms.CharField(max_length=200, widget=forms.Textarea(attrs={
        "placeholder": "Ingrese el motivo de la actualizacion"
    }), required=False)


    class Meta:
        model = Paciente
        exclude = ['created_by', 'created_at', 'updated_by', 'updated_at']
        widgets = {
            'fecha_nacimiento': forms.DateInput(attrs={'type':'date'}),
            'telefono': forms.TextInput(attrs={'placeholder': 'EJ: 920036589'}),
            'direccion': forms.TextInput(attrs={'placeholder': 'Calle, número, depto...'}),
            'peso': forms.NumberInput(attrs={'placeholder': 'En Kilogramos'}),
            'altura': forms.NumberInput(attrs={'placeholder':'En Centimetros'}),
            'nombre': forms.TextInput(attrs={'placeholder': 'Ej: Rosalia Alejandra'}),
            'primer_apellido': forms.TextInput(attrs={'placeholder': 'Apellido del Paciente'}),
            'segundo_apellido': forms.TextInput(attrs={'placeholder': 'Apellido del Paciente'}),
        }
        
        # Textos mostrados debajo de cada campo al renderizarlo
        help_texts = {
            'cesfam': 'Si no posee dejar en blanco',
            'comuna': 'Si no aparece la comuna dejar en blanco',
            'identificacion': 'Si es Rut sin puntos y con guion',
            'altura': 'En centimetros',
            'peso': 'En Kilogramos',
            'telefono': 'Para nacionales añada el 9. No requiere +56.',
            'nacionalidad': "Si no aparece la nacionalidad marcar OTRA",
            'direccion': 'Si no posee dejar en blanco.',
            'peso': 'Si no proporciona el peso en Kilogramos los calculos del IMC tendran errores'
            }
        

        # El texto del label que describe o indica que valor recibe el campo
        labels = {
            'documento': "Tipo Documento",
            'identificacion': 'N° de documento',
            'tipo': 'Tipo de Paciente',
            'descapacitado': 'Descapacitad@',
            'pueblo_originario': 'Pueblo Originario',
            'privada_de_libertad': 'Privada de Libertad',
            'transexual': 'Transexual',
            'fecha_nacimiento': 'Fecha de Nacimiento',
            'telefono': 'Teléfono',
            'direccion': 'Dirección',
            
        }


    def clean_motivo(self):
        motivo = self.cleaned_data.get('motivo')
        if self.instance.pk and not motivo:
            raise forms.ValidationError("Debe especificar el motivo de la actualizacion")
        return motivo


    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        if nombre:
            return nombre.strip().capitalize()
        return nombre
    
    
    def clean_primer_apellido(self):
        primer_apellido = self.cleaned_data.get('primer_apellido')
        if  primer_apellido:
            return primer_apellido.strip().capitalize()
        return primer_apellido
    

    def clean_segundo_apellido(self):
        segundo_apellido = self.cleaned_data.get('nombre')
        if segundo_apellido:
            return segundo_apellido.strip().capitalize()
        return segundo_apellido


    def clean_peso(self):
        peso = self.cleaned_data.get('peso')
        
        if not peso:
            peso = 0
            return peso

        if not peso > 0:
            raise forms.ValidationError("Una persona no puede pesar menos de 0")
        return peso


    def clean_altura(self):
        altura = self.cleaned_data.get('altura')
        if not altura:
            altura = 0
            return altura
        
        if not altura > 0:
            raise forms.ValidationError("Una persona no puede ser un minion")
        
        return altura


    def clean_telefono(self):
        telefono = self.cleaned_data.get('telefono')
        if not telefono:
            return telefono


        try:
            if telefono.startswith("+"):
                telefono_parseado = phonenumbers.parse(telefono)
            else:
                # si viene sin + asumiremos que es chileno aunque no lo sea
                telefono_parseado = phonenumbers.parse(telefono, "CL")
        except phonenumbers.NumberParseException as e:
            # Si fallo el parse puede ser por estos motivos:
            if e.error_type == e.INVALID_COUNTRY_CODE:
                raise forms.ValidationError("Codigo de pais invalido para el numero proporcionado")
            elif e.error_type == e.NOT_A_NUMBER:
                raise forms.ValidationError("El número telefonico no puede contener letras")
            elif e.error_type == e.TOO_LONG:
                raise forms.ValidationError("El número es demasiado largo para ser valido")
            elif e.error_type == e.TOO_SHORT_NSN or e.error_type == e.TOO_SHORT_AFTER_IDD:
                raise forms.ValidationError("El número es demasiado corto para ser valido")
            else:
                raise forms.ValidationError("El número no es valido")
            
        # Una vez tenemos el nùmero parseado en un formato valido y soportado por la libreria
        # evaluamos si ese número podria existir en ese pais que se especifico por su codigo
        # si regresa False es pq es imposible que exista como +56 9 11111111 que cumple la estructura de chile
        # pero no es valido
        if not phonenumbers.is_valid_number(telefono_parseado):
            raise forms.ValidationError("El número no es valido. Ingrese un numero que pueda existir en el pais")

        # Si pasa las validaciones lo regresamos en el formato aceptado internacionalmente E.164 que es usado
        # en todos los sistemas como GMAIL, WHATSAPP, ANDROID.
        return phonenumbers.format_number(
            telefono_parseado, 
            phonenumbers.PhoneNumberFormat.E164
        )
        

        
    def clean_fecha_nacimiento(self):
        fecha_nacimiento = self.cleaned_data.get('fecha_nacimiento')
        print(fecha_nacimiento)
        if fecha_nacimiento:
            fecha_actual = timezone.now().date()
            print(fecha_actual)
            edad = fecha_actual.year - fecha_nacimiento.year
            if fecha_nacimiento >= fecha_actual:
                raise forms.ValidationError('La fecha de nacimiento no puede superar a la fecha actual')
            
            if edad < 10 or edad > 60:
                raise forms.ValidationError('No se puede registar una persona menor a 10 años o mayor a 60')
                
        return fecha_nacimiento
    


    def clean(self):
        cleaned = super().clean()
        documento = cleaned.get('documento')
        identificacion = cleaned.get('identificacion')

        # RECORDAR EL CLEANED ES DATA YA ES VALIDADA Y COMO SE ALMACENARA EN LA DB
        # POR ESO EN MAYUSCULA
        if documento == "RUT":
            if not identificacion:
                self.add_error('identificacion', 'Debe proporcionar el rut')
            rut_valido = validators.validar_rut(identificacion)
            if not rut_valido[0]:
                self.add_error('identificacion', rut_valido[1])

        elif documento == "PAS":
            if not identificacion or len(identificacion) < 5:
                self.add_error('identificacion','Debe proporcionar el pasaporte completo')
        elif documento == "EXT":
            if not identificacion or len(identificacion) < 3:
                self.add_error('identificacion', 'Debe proporcionar codigo extranjero')
        elif documento == "TMP":
            codigo_temporal = utils.generar_codigo_temporal()
            cleaned['identificacion'] = codigo_temporal
        else:
            self.add_error('identificacion', 'Debe seleciona un tipo de documento')
    
        return cleaned