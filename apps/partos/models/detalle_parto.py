from django.db import models

# ESTE MODELO NO TIENE FORMULARIO
class TipoDeIngreso(models.Model):
    nombre = models.CharField(max_length=50, unique=True)
    
    def __str__(self):
        return self.nombre


# ESTE MODELO NO TIENE FORMULARIO
class GrupoRobson(models.Model):
    grupo = models.CharField(max_length=50, unique=True)
    descripcion = models.TextField()
    def __str__(self):
        return f"{self.grupo} | Descripción: {self.descripcion}"

# ESTE MODELO NO TIENE FORMULARIO
class Complicacion(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField()

    def __str__(self):
        return self.nombre


# ESTE MODELO NO TIENE FORMULARIO
class ViaNacimiento(models.Model):
    tipo = models.CharField(max_length=60, unique=True)
    descripcion = models.TextField()
    
    def __str__(self):
        return self.tipo


