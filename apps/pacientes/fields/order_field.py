from django.core.exceptions import ObjectDoesNotExist
from django.db import models

# Campo propio que se encarga de ordenar los objetos dentro de un grupo determinado
# asignando automaticamente un numero entero positivo que representa su lugar en el orden
class OrderField(models.PositiveIntegerField):

    def __init__(self, for_fields=None, *args, **kwargs):
        self.for_fields = for_fields
        super().__init__(*args, **kwargs)

    # Pre save ejecuta la logica antes de guardar el objeto en su modelo, para el campo OrderField
    # y el valor que retorne este metodo es el que se almacenara en el campo que le asigno el OrderField
    # en la base de datos
    def pre_save(self, model_instance, add):
         # Si el campo ya tiene valor, no hagas nada.
        if not (getattr(model_instance, self.attname) is None):
            return super().pre_save(model_instance, add)

        qs = self.model.objects.all()

        # Si hay campos para agrupar, filtramos por ellos
        if self.for_fields:
            query = {
                field: getattr(model_instance, field)
                for field in self.for_fields
            }
            qs = qs.filter(**query)

        # Ahora buscamos el último del grupo (o global si no hay grupo)
        try:
            last_item = qs.latest(self.attname)
            value = getattr(last_item, self.attname) + 1

        except ObjectDoesNotExist:
            # Primer elemento del grupo
            value = 1

        # Asignamos ese valor al campo antes de guardar
        setattr(model_instance, self.attname, value)
        return value