from django.db import models
from django.conf import settings
from django.core.validators import MaxValueValidator
from simple_history.models import HistoricalRecords

from .detalle_parto import (Complicacion, 
                            GrupoRobson, TipoDeIngreso,
                            ViaNacimiento)
from apps.pacientes.models.gestacion import Gestacion


# Datos ingresados durante el trabajo de parto o parto
class Parto(models.Model):

# Esto no respeta la normalizacion de DB, pero en otra version se les hace un modelo
# a cada una
   class TipoRotura(models.TextChoices):
      ESPONTANEA = 'espontanea', "Espontánea"
      ARTIFICIAL = 'artificial', 'Artificial'
    

   class InicioTrabajoParto(models.TextChoices):
      ESPONTANEO = 'espontanea', 'Espontánea'
      INDUCIDO_FARMACOLOGICA = 'inducido_far', 'Inducido Farmacologicamente'
      INDUCIDO_MECANICA = 'inducido_mec', 'Inducido Mecanicamente'
      CONDUCIDO = 'conducido', 'Conduccion Oxitóxica'


   class TipoRegimen(models.TextChoices):
      CERO = 'cero', 'Cero'
      LIQUIDO = 'liquido', 'Liquido'
      COMUN =  'comun', 'Comun'
      OTRO = 'otro', 'Otro'


   class EstadoParto(models.TextChoices):
      CERRADO = 'terminado', 'Terminado'
      INGRESO = 'ingreso', 'Ingreso'
      ACTIVO = 'activo', 'Activo'
      EXPULSIVO = 'expulsivo', 'Expulsivo'
      ALUMBRAMIENTO = 'alumbramiento', 'Alumbramiento'
      PUERPERIO = 'puerperio', 'Puerperio Inmediato'


   class TipoAcompaniante(models.TextChoices):
      SIN_ACOMPANIANTE = 'sin', 'Sin Acompaniante'
      DURANTE_TRABAJO_PARTO = 'trab_parto', 'Durante Trabajo de Parto'
      SOLO_EXPULSIVO = 'solo_expul', 'Solo Expulsivo'


   class PosicionParto(models.TextChoices):
      SEMISENTADA = 'semisentada', 'Semisentada'
      SENTADA = 'sentada', 'Sentada'
      LITOTOMIA = 'litotomia', 'Litotomia'
      D_DORSAL = 'dorsal', 'D.Dorsal'
      CUADRUPEDA = 'cuadrupeda', 'Cuadrúpeda'
      D_LATERAL = 'lateral', 'D.Lateral'
      DE_PIE = 'de pie', 'De Pie'
      CUCLILLAS = 'cuclillas', 'Cuclillas'
      OTRO = 'otro', 'Otro'


   # NO VAN EN EL FORMULARIO
   created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT,
                              related_name='partos', null=True)
   created_at = models.DateTimeField(auto_now_add=True)

   updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, 
                                 related_name='partos_actualizados', null=True)
   updated_at = models.DateTimeField(auto_now=True)


   tipo_de_ingreso = models.ForeignKey(TipoDeIngreso, on_delete=models.PROTECT, related_name='partos')
   grupo_robson = models.ForeignKey(GrupoRobson, on_delete=models.PROTECT, related_name="partos", blank=True, null=True)
   via_nacimiento = models.ForeignKey(ViaNacimiento, on_delete=models.PROTECT, related_name="partos")
   gestacion = models.OneToOneField(Gestacion, on_delete=models.PROTECT, related_name="parto")
   complicaciones = models.ManyToManyField(Complicacion, related_name="partos", blank=True)
   hora_inicio = models.DateTimeField()
   numero_aro = models.PositiveSmallIntegerField(default=0)
   
   n_tactos_vaginales = models.PositiveSmallIntegerField(validators=[MaxValueValidator(40)], default=0)
   
   rotura_membrana = models.CharField(max_length=50,
                                    choices=TipoRotura.choices,
                                    default=TipoRotura.ESPONTANEA)
   
   estado = models.CharField(max_length=30,
                           choices=EstadoParto.choices,
                           default=EstadoParto.INGRESO)

   posicion = models.CharField(max_length=50,
                              choices=PosicionParto.choices,
                              default=PosicionParto.OTRO)
   tipo_regimen = models.CharField(max_length=50,
                                   choices=TipoRegimen.choices,
                                   default=TipoRegimen.CERO)
   inicio_parto = models.CharField(max_length=50, 
                                   choices=InicioTrabajoParto.choices,
                                   default=InicioTrabajoParto.ESPONTANEO)

   observaciones = models.TextField(blank=True, max_length=1000)

   # Acordarse que estos campos deben guardarse con timedelta y en minutos
   tiempo_membrana_rota = models.DurationField()
   tiempo_dilatacion = models.DurationField()
   tiempo_expulsivo = models.DurationField()
   # NO VA EN EL FORMULARIO
   edad_madre = models.PositiveSmallIntegerField()
   monitor = models.BooleanField(default=False)
   entrega_placenta = models.BooleanField(default=False)
   tipo_acompaniante = models.CharField(max_length=50, 
                                        choices=TipoAcompaniante.choices,
                                        default=TipoAcompaniante.SIN_ACOMPANIANTE)
   
   libertad_movimiento = models.BooleanField(default=False)

   semanas_gestacion = models.PositiveSmallIntegerField(blank=True, null=True) # Este field se obtiene de el calculo de semanas de la gestacion con su metodo

   # lo oculto y no lo exigo en el formulario ya que no hay tiempo para reconstruir database
   acompaniante = models.BooleanField(default=False, blank=True, null=True)
   ttc = models.BooleanField(default=False)
   # Field para no exigir en el db por el simple echo de que no quiero modificar la base de datos completas pq no queda tiempo
   induccion = models.BooleanField(default=False, blank=True, null=True)
   aceleracion = models.BooleanField(default=False, blank=True, null=True)
   oxitocina_profilactica = models.BooleanField(default=False)
   uso_sala_saip = models.BooleanField(default=False)
   
   # Un atributo o campo que tendran nuestros objetos del modelo Parto, que les otorgara un manager que les permitira realizar consultas
   # sobre todos los registros que tengan asociados de la tabla espejo que se creara del modelo Parto, donde cada registro representa a una version
   # del objeto del modelo Parto en cuestion. Ahora la asociacin no ocurre con un foreignkey estricto de BASE DE DATOS, si no que si efectivamente los registros
   # de la tabla secundaria, espejo o historica tiene un field que contiene la clave primaria del objeto del cual es snapshot pero sin ser tipo foreignkey para evitar que si se elimina
   # el objeto del modelo principal de Parto no se elimine su historico y asi podamos usar un historico para reconstruir un objeto eliminado del modelo Principal Parto 
   # con todos los datos de ese registro historico o del que seleccionemos para restaurarlo.
   history = HistoricalRecords()



   def __str__(self):
      # Diseño optimizado para Auditoría: Tipo + ID + Paciente
      paciente = self.gestacion.paciente
      nombre = f"{paciente.nombre} {paciente.primer_apellido}"
      return f"Parto #{self.pk} - {nombre} ({paciente.identificacion})"


   def save(self, *args, **kwargs):
      if not self.edad_madre:
         self.edad_madre = self.gestacion.paciente.calcular_edad_paciente()
      
      if not self.semanas_gestacion:
         self.semanas_gestacion = self.gestacion.obtener_semanas_gestacion()
         if self.semanas_gestacion:
            self.semanas_gestacion = self.semanas_gestacion.get('semanas')

      super().save(*args, **kwargs)



'''
10. Integridad de FK/M2M
   - Validar que las instancias de tipo_de_ingreso, robson, via_nacimiento, profesionales existan.
'''