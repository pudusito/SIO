from django.db import models
from django.conf import settings
from django.utils import timezone
from simple_history.models import HistoricalRecords

from .paciente import Paciente
from ..fields import OrderField


tipo_documento = ["RUT",  "PAS", "EXT", "TEMP"]


class Gestacion(models.Model):
    class Meta:
        verbose_name = "Gestacion"
        verbose_name_plural = "Gestaciones"


    class Riesgo(models.TextChoices):
        BAJO = "bajo", "Bajo Riesgo"
        MEDIO = "medio", "Riesgo Moderado"
        ALTO = "alto", "Alto Riesgo"


    class OrigenDatacion(models.TextChoices):
        FUR = "fur", "FUR"
        ECO = "eco", "ECO"
        SIN_DATACION = 'sin', 'Sin Datacion Disponible'

    class Estado(models.TextChoices):
        TERMINADA = 'terminada', 'Terminada'
        ABORTO = 'aborto', 'Aborto'
        EN_CURSO = 'curso', 'En Curso'

    paciente = models.ForeignKey(Paciente, 
                                 on_delete=models.CASCADE, 
                                 related_name="gestaciones", null=True)
    
    # ESTOS CAMPOS NO VAN EN EL FORMULARIO ******************************
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="gestaciones", null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='gestaciones_actualizadas', null=True)
    updated_at = models.DateTimeField(auto_now=True)

    numero_fetos = models.PositiveSmallIntegerField()

    riesgo = models.CharField(max_length=10, 
                              choices=Riesgo.choices,
                              default=Riesgo.BAJO)
    estado = models.CharField(max_length=10,
                              choices=Estado.choices,
                              default=Estado.EN_CURSO)


    # Matrona o usuario aqui elige que metodo se uso para calcular la fecha de inicio 
    # de la edad de gestacion si fue FUR o ECO
    origen_datacion = models.CharField(max_length=3,
                                       choices=OrigenDatacion.choices,
                                      default=OrigenDatacion.SIN_DATACION,
                                       help_text="La fecha de inicio de gestación se tomará según el origen que seleccione: FUR o ECO.")

    # Fecha de ultima regla
    fur = models.DateField(null=True, blank=True)
    # Fecha de cuando se tomo la ecografia para obtener edad gestacional
    fecha_eco = models.DateField(null=True, blank=True)
    # Semanas y dias estimados que arrojo la eco de edad gestacional
    semanas_eco = models.PositiveSmallIntegerField(null=True, blank=True)
    dias_eco = models.PositiveSmallIntegerField(null=True, blank=True)
    
    
    # NO VA EN EL FORMULARIO
    fecha_inicio_gestacion = models.DateField(null=True, blank=True)

    numero_gestacion = OrderField(for_fields=['paciente'], blank=True)

    enfermedad_cardiaca = models.BooleanField(default=False)
    hipertension = models.BooleanField(default=False)
    diabetes = models.BooleanField(default=False)
    multiple = models.BooleanField(default=False)

    
    history = HistoricalRecords()


    def __str__(self):

        if not self.pk:
            return f"Paciente: {self.paciente.obtener_nombre_completo()} {self.paciente.identificacion}"
        return f"Paciente: {self.paciente.obtener_nombre_completo()} | Rut: {self.paciente.identificacion} | Gestación: #{self.pk}"

    def save(self, *args, **kwargs):
        # Antes de almacenar una gestacion verificamos que debe guardarse segun el oriden de datacion
        if self.origen_datacion == self.OrigenDatacion.FUR:
            if self.fur:
                self.fecha_inicio_gestacion = self.fur
        elif self.origen_datacion == self.OrigenDatacion.ECO:
            if self.semanas_eco is not None and self.dias_eco is not None and self.fecha_eco:
                dias_totales = self.semanas_eco * 7 + self.dias_eco
                self.fecha_inicio_gestacion = self.fecha_eco - timezone.timedelta(days=dias_totales)

        super().save(*args, **kwargs)


    def obtener_semanas_gestacion(self):
        if not self.fecha_inicio_gestacion:
            return None
        
        fecha_actual = timezone.localdate()
        dias_totales = (fecha_actual - self.fecha_inicio_gestacion).days
        # cuantas semanas caben en los dias totales
        semanas_gestacion = dias_totales // 7
        # el resto lo que sobra o los dias que sobran los tomamos como dias
        dias_gestacion = dias_totales % 7
        return {
            'semanas': semanas_gestacion,
            'dias': dias_gestacion,
            'total_dias': dias_totales,
        }
