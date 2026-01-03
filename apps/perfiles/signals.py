from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import SupervisorPerfil, MatronaPerfil

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def crear_perfil(sender, instance, created, *args):
    if not created:
        return 
    
    if instance.es_matrona:
        MatronaPerfil.objects.get_or_create(user=instance)
        return
    
    if instance.es_supervisor:
        SupervisorPerfil.objects.get_or_create(user=instance)
        return