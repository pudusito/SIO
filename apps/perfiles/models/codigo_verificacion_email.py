from django.db import models
from django.conf import settings


class CodigoVerificacionEmail(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="codigos_email")
    code = models.PositiveSmallIntegerField()
    create_at = models.DateTimeField(auto_now_add=True)
    expired_at = models.DateTimeField()
