from django.http import Http404

from apps.pacientes.models import Paciente, Gestacion
from apps.partos.models import Parto
from apps.recien_nacidos.models import RecienNacido


MODELOS_AUDITADOS = {
        'paciente': Paciente,
        'gestacion': Gestacion,
        'parto': Parto,
        'recien_nacido': RecienNacido
    }

class DeterminarModeloAuditarMixin:

    def dispatch(self, request, model_name=None, *args, **kwargs):
        self.modelo_a_auditar =MODELOS_AUDITADOS.get(model_name)
        if not self.modelo_a_auditar:
            raise Http404()
        self.model = self.modelo_a_auditar
        return super().dispatch(request, *args, **kwargs)
