from django.db import models
from django.conf import settings


class Perfil(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='%(class)s')
    telefono = models.CharField(max_length=15, blank=True)
    foto_perfil = models.FileField(upload_to='imagen_perfil/', blank=True)    
    fecha_contratacion = models.DateField(blank=True)
    activo = models.BooleanField(default=True)
    rut = models.CharField(max_length=16, unique=True)


    class Meta:
        abstract = True

    