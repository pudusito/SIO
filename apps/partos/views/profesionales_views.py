from django.views.generic import TemplateView, ListView, CreateView
from django.urls import reverse_lazy, reverse
from django.shortcuts import get_object_or_404
from django.contrib import messages

from core.mixins import MatronaRequiredMixin, MatronaSupervisorRequiredMixin


from apps.partos.models.profesional import Profesional, Participacion
from apps.partos.models.profesional import Parto
# Importa el form que acabamos de crear
from apps.partos.forms.profesional_form import ProfesionalForm

class MenuInicioProfesionalesView(MatronaSupervisorRequiredMixin, TemplateView):
    """Renderiza el menú de opciones de Profesionales"""
    template_name = 'partos/inicio_profesionales.html'

class ListarProfesionalesView(MatronaSupervisorRequiredMixin, ListView):
    """Renderiza la tabla de profesionales"""
    model = Profesional
    template_name = 'partos/listar_profesionales.html'
    context_object_name = 'profesionales' # Al ser ListView, ahora sí enviará esta variable
    paginate_by = 10
    
class CrearProfesionalView(MatronaRequiredMixin, CreateView):
    model = Profesional
    form_class = ProfesionalForm
    template_name = 'partos/formulario_profesionales.html'
    # Al terminar de agregar, nos lleva al listado para ver al nuevo integrante
    success_url = reverse_lazy('profesionales:listar')



class CrearParticipacion(MatronaRequiredMixin, CreateView):
    model = Participacion
    fields = ['profesional']
    template_name = 'partos/formulario_participacion.html'  
    

    def form_valid(self, form):
        parto = get_object_or_404(Parto, pk=self.kwargs.get('parto_id'))
        form.instance.parto = parto
        messages.success(self.request, "Participacion registrada correctamente")
        return super().form_valid(form)
    

    def get_success_url(self):
        return reverse('parto:detalles_parto', kwargs={'pk': self.kwargs.get('parto_id')})