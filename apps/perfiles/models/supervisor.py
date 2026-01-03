from django.db import models
from .perfil import Perfil


class SupervisorPerfil(Perfil):
    unidad_supervisacion = models.CharField(max_length=100, blank=False)


    class Meta:
        verbose_name = "Perfil Supervisor"
        verbose_name = "Perfiles Supervisores"


    def __str__(self):
        return f"Supervisor: {self.user.get_full_name()}"