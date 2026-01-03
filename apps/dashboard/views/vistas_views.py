from django.shortcuts import render
from django.views.generic import TemplateView, View
from django.utils import timezone

from core.mixins import SupervisorRequiredMixin
from ..config import Gestacion, Paciente, Parto, Profesional, RecienNacido

def index(request):
    return render(request, 'index.html')

class PacientesView(SupervisorRequiredMixin, View):
    template_name = 'layouts/pacientes.html'

    def get(self, request, *args, **kwargs):
        fecha_actual = timezone.now()
        pacientes = Paciente.objects.prefetch_related('gestaciones')
        pacient_riesg_activo = pacientes.filter(gestaciones__estado="curso", gestaciones__riesgo="alto").distinct().count()
        gest_activa = pacientes.filter(gestaciones__estado='curso').count()
        pacient_anio = pacientes.filter(created_at__year=fecha_actual.year).count()
        partos = Parto.objects.all()
        edad_madre_18_25 = partos.filter(edad_madre__gte=18, edad_madre__lte=25).count()
        edad_madre_26_35 = partos.filter(edad_madre__gte=26, edad_madre__lte=35).count()
        edad_madre_36_45 = partos.filter(edad_madre__gte=36, edad_madre__lte=45).count()
        edad_madre_56_mas = partos.filter(edad_madre__gte=56).count()
        rango_edades = str([edad_madre_18_25, edad_madre_26_35, edad_madre_36_45, edad_madre_56_mas])

        gestaciones = Gestacion.objects.all()
        gestaciones_enero = gestaciones.filter(created_at__year=fecha_actual.year, created_at__month=1).count()
        gestaciones_febrero = gestaciones.filter(created_at__year=fecha_actual.year, created_at__month=2).count()
        gestaciones_marzo = gestaciones.filter(created_at__year=fecha_actual.year, created_at__month=3).count()
        gestaciones_abril = gestaciones.filter(created_at__year=fecha_actual.year, created_at__month=4).count()
        gestaciones_mayo = gestaciones.filter(created_at__year=fecha_actual.year, created_at__month=5).count()
        gestaciones_junio = gestaciones.filter(created_at__year=fecha_actual.year, created_at__month=6).count()
        gestaciones_julio = gestaciones.filter(created_at__year=fecha_actual.year, created_at__month=7).count()
        gestaciones_agosto = gestaciones.filter(created_at__year=fecha_actual.year, created_at__month=8).count()
        gestaciones_septiembre = gestaciones.filter(created_at__year=fecha_actual.year, created_at__month=9).count()
        gestaciones_octubre = gestaciones.filter(created_at__year=fecha_actual.year, created_at__month=10).count()
        gestaciones_noviembre = gestaciones.filter(created_at__year=fecha_actual.year, created_at__month=11).count()
        gestaciones_diciembre = gestaciones.filter(created_at__year=fecha_actual.year, created_at__month=12).count()

        gestaciones_anio = str([gestaciones_enero, gestaciones_febrero, gestaciones_marzo, gestaciones_abril, gestaciones_mayo,
                                gestaciones_junio, gestaciones_julio, gestaciones_agosto, gestaciones_septiembre, gestaciones_octubre,
                                gestaciones_noviembre, gestaciones_diciembre])


        # pacientes registrados este año
        pacientes = pacientes.filter(created_at__year=fecha_actual.year, created_at__month=fecha_actual.month)

        context_data = {
            'kpipaciente1': pacient_riesg_activo,
            'kpipaciente2': gest_activa,
            'kpipaciente3': pacient_anio,
            'chartpaciente2': rango_edades,
            'chartpaciente1': gestaciones_anio,
            'pacientes': pacientes
        }
        return render(request, self.template_name, context_data)


class PartosView(TemplateView):
    template_name = 'layouts/partos.html'

class PerfilesView(TemplateView):
    template_name = 'layouts/perfiles.html'

class RecienNacidosView(TemplateView):
    template_name = 'layouts/recien_nacidos.html'

class ReportesView(TemplateView):
    template_name = 'layouts/reportes.html'

class ProfesionalesView(TemplateView):
    template_name = 'layouts/profesionales.html'


class TestView(TemplateView):
    template_name = '500.html'


