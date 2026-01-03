from django.db import models
from .perfil import Perfil
from .turno import Turno

class MatronaPerfil(Perfil):
    # Supervisor debe poder editar los turnos pero no eliminarlos
    turno = models.ForeignKey(Turno, on_delete=models.PROTECT, 
                              help_text="No puedes eliminar un TURNO que ya halla sido asignado a una Matrona", 
                              related_name='turno')
    especialidad = models.CharField(max_length=100, blank=True)
    cargo = models.CharField(max_length=100, blank=True)
    unidad_asignada = models.CharField(max_length=100, blank=True)

    class Meta:
        verbose_name = "Perfil Matrona"
        verbose_name_plural = "Perfiles Matronas"

    def __str__(self):
        return f"Matrona {self.especialidad}: {self.user.get_full_name()}"