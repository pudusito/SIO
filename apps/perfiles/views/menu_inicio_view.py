from django.views.generic import TemplateView
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin

from apps.pacientes.models import Paciente
from apps.partos.models import Parto
from apps.recien_nacidos.models import RecienNacido

class MostrarPantallaPrincipalView(LoginRequiredMixin, TemplateView):
    template_name="principal.html"


    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        hoy = timezone.now().date()
        mes = hoy.month
        semana = hoy.isocalendar()[1]
        pc_mes = Paciente.objects.filter(created_at__month=mes).count()
        pt_mes = Parto.objects.filter(created_at__month=mes).count()
        rn_mes = RecienNacido.objects.filter(created_at__month=mes).count()
        pc_sem = Paciente.objects.filter(created_at__week=semana).count()
        pt_sem = Parto.objects.filter(created_at__week=semana).count()
        rn_sem = RecienNacido.objects.filter(created_at__week=semana).count()

        context['pc_mes'] = pc_mes
        context['pt_mes'] = pt_mes
        context['rn_mes'] = rn_mes
        context['pc_sem'] = pc_sem
        context['pt_sem'] = pt_sem
        context['rn_sem'] = rn_sem

        return context