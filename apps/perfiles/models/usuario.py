from django.contrib.auth.models import AbstractUser
from django.db import models


class Usuario(AbstractUser):
    email = models.EmailField("correo", unique=True, max_length=254)
    last_name2 = models.CharField(max_length=30)
    first_login = models.BooleanField(default=True)
    es_matrona = models.BooleanField(default=False)
    es_supervisor = models.BooleanField(default=False)


    # username_field es el atributo que define que campo usara como username el modelo Usuario, es decir
    # el campo que se usara para identificar al usuario y autenticarlo
    USERNAME_FIELD = 'email' # email usaremos para validar su identidad UwU
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    def __str__(self):
        return self.get_full_name()


    def get_full_name(self):
        full_name = f"{self.first_name} {self.last_name} {self.last_name2}"
        return full_name.strip()