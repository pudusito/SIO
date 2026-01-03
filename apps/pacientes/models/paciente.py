from decimal import Decimal, ROUND_UP
from django.db import models
from django.utils import timezone
from django.conf import settings
from simple_history.models import HistoricalRecords


# ESTE MODELO NO TIENE FORMULARIO
class TipoPaciente(models.Model):
    nombre = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nombre


# ESTE MODELO NO TIENE FORMULARIO
class Comuna(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    
    class Meta:
        ordering = ['nombre']

    def __str__(self):
        return self.nombre

# ESTE MODELO NO TIENE FORMULARIO
class Nacionalidad(models.Model):
    nombre = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ['nombre']
    
    def __str__(self):
        return self.nombre

# ESTE MODELO NO TIENE FORMULARIO
class Cesfam(models.Model):
    nombre = models.CharField(max_length=120, unique=True)
    comuna = models.ForeignKey(Comuna, on_delete=models.PROTECT)

    class Meta:
        ordering = ['comuna__nombre', 'nombre']

    def __str__(self):
        return f"{self.nombre} ({self.comuna})"


class Paciente(models.Model):

    class Sexo(models.TextChoices):
        MASCULINO = 'M', 'Masculino'
        FEMENINO = 'F', 'Femenino'
        OTRO = 'O', 'otro'

    class Actividad(models.TextChoices):
        BAJA = 'baja', 'Baja'
        MODERADA = 'moderada', 'Moderada'
        ALTA = 'alta', 'Alta'

    class TipoDocumento(models.TextChoices):
        RUT = 'RUT', 'Rut'
        PAS = 'PAS', 'Pasaporte'
        EXT = 'EXT', 'Documento extranjero'
        TMP = 'TMP', 'Sin documento / Temporal'  

    # NO VA EN EL FORMULARIO
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='pacientes', null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='pacientes_actualizados', null=True)
    updated_at = models.DateTimeField(auto_now=True)

    # fonasa, isapre, etc.
    tipo = models.ForeignKey(TipoPaciente, on_delete=models.PROTECT, related_name='paciente')
    
    # Puede quedar null ese valor ya que el cesfam comuna o nacionalidad de ese paciente puede desaparecer 
    # y si desaparece simplemente se queda sin esa info pero no deberia desaparecer el paciente
    nacionalidad = models.ForeignKey(Nacionalidad, on_delete=models.SET_NULL, related_name='paciente', null=True)
    comuna = models.ForeignKey(Comuna, on_delete=models.SET_NULL, related_name='paciente', null=True, blank=True)
    cesfam = models.ForeignKey(Cesfam, on_delete=models.SET_NULL, related_name='paciente', null=True, blank=True)
    direccion = models.CharField(max_length=150, blank=True)
    telefono = models.CharField(max_length=15, blank=True) # Validar luego el formato del telefono
    nombre = models.CharField(max_length=100)
    primer_apellido = models.CharField(max_length=100)
    segundo_apellido = models.CharField(max_length=100)
    
    # Info Documento
    documento = models.CharField(max_length=3, 
                                 choices=TipoDocumento.choices, 
                                 default=TipoDocumento.RUT)
    identificacion = models.CharField(max_length=50, blank=True)

    fecha_nacimiento = models.DateField()
    descapacitado = models.BooleanField(default=False)
    pueblo_originario = models.BooleanField(default=False)
    privada_de_libertad = models.BooleanField(default=False)
    transexual = models.BooleanField(default=False)
    plan_de_parto = models.BooleanField(default=False)
    visita_guiada = models.BooleanField(default=False)
    peso = models.DecimalField(max_digits=5, decimal_places=2, blank=True, default=0)
    altura = models.DecimalField(max_digits=5, decimal_places=2, blank=True, default=0)
    actividad = models.CharField(max_length=9,
                                 choices=Actividad.choices,
                                 default=Actividad.BAJA)
    sexo = models.CharField(max_length=10,
                            choices=Sexo.choices,
                            default=Sexo.FEMENINO)

    history = HistoricalRecords()

    def __str__(self):
        return f'{self.documento}: {self.identificacion} | Paciente: {self.obtener_nombre_completo()}'
    

    def obtener_nombre_completo(self):
        return f'{self.nombre} {self.primer_apellido} {self.segundo_apellido}'

    def calcular_imc(self):
        if self.altura and self.peso:
            estatura_metros = self.altura / Decimal("100")
            return (self.peso / (estatura_metros ** 2)).quantize(Decimal("0.01"), rounding=ROUND_UP)
    

    def calcular_edad_paciente(self):
       
        hoy = timezone.localdate()
        edad = hoy.year - self.fecha_nacimiento.year
        
        if self.fecha_nacimiento.month > hoy.month or (self.fecha_nacimiento.month == hoy.month and self.fecha_nacimiento.day > hoy.day):
            edad -= 1
        return edad

    class Meta:
        # No puede haber una identificación repetida dentro del mismo grupo de tipo de documento
        unique_together = ('documento', 'identificacion')   
        # segun que esto mejora rendimiento investigar luego
        indexes = [
            models.Index(fields=['documento', 'identificacion'])
        ]

    '''
    VALIDACIONES QUE FALTAN:
    Tu modelo debería validar:

        ✔ que la fecha de nacimiento no sea futura
        ✔ que el teléfono tenga formato válido (+56…)
        ✔ que el peso sea > 0
        ✔ que la altura sea > 0
        ✔ que el IMC sea razonable (opcional)
    '''