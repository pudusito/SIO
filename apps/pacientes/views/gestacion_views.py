from django.views.generic import CreateView, ListView, TemplateView, UpdateView, DeleteView
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import HttpResponse
from django.db.models import Q, Value, F
from django.db.models.functions import Concat
from django.contrib import messages
from django.urls import reverse_lazy
from dal import autocomplete

from core.forms import MotivoForm
from core.mixins import MatronaSupervisorRequiredMixin, MatronaRequiredMixin
from ..models import Gestacion, Paciente
from ..forms import GestacionForm



class MenuInicioGestacionesView(MatronaSupervisorRequiredMixin, TemplateView):
    template_name = "pacientes/inicio_gestaciones.html"


class ListarGestacionesView(MatronaSupervisorRequiredMixin, PermissionRequiredMixin,ListView):
    model = Gestacion
    template_name = "pacientes/listar_gestaciones.html"
    context_object_name = 'gestaciones'
    paginate_by = 8

    permission_required = "pacientes.view_gestacion"
    raise_exception = True

    # Por cada una de las 10 o 15 gestaciones listadas en la pagina se precarga el paciente que tiene asociado
    def get_queryset(self):
        qs = self.model.objects.select_related('paciente')
        qs = qs.annotate(nombre_completo_paciente=Concat('paciente__nombre', Value(' '), 'paciente__primer_apellido', Value(' '), 'paciente__segundo_apellido'), 
                         identificacion_paciente=F('paciente__identificacion'))

        query_params = self.request.GET.copy()
        if 'page' in query_params:
            query_params.pop('page')
        self.query_string = query_params.urlencode()

        self.query = self.request.GET.get('query')

        self.plan_de_parto = self.request.GET.get('pp')
        
        if self.query and '.' in self.query:
            self.query = self.query.replace('.', '')




        # Cabros si se manda desde el navegador un params llamado query filtramos si no, no lo hacemos
        if self.query:
            qs = qs.filter(Q(nombre_completo_paciente__icontains=self.query) | Q(identificacion_paciente__startswith=self.query))

        return qs.order_by('-created_at')

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context['query_string'] = self.query_string
        context['query'] = self.query
        return context

class CrearGestacionView(MatronaRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Gestacion
    template_name = "pacientes/formulario_gestacion.html"
    form_class = GestacionForm
    
    permission_required = "pacientes.add_gestacion"
    raise_exception = True

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.updated_by = self.request.user
        form.save()
        return HttpResponse('<h1>Gestacion Almacenada correctamente</h1>')



# view encargada se ejecutar la logica para actualizar los datos de un paciente
class ActualizarGestacionView(MatronaRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Gestacion
    template_name = "pacientes/formulario_gestacion.html"
    form_class = GestacionForm
    permission_required= "pacientes.change_gestacion"
    raise_exception = True
    context_object_name = "gestacion"
    success_url = reverse_lazy("gestacion:listar_gestaciones")

    def form_valid(self, form):
        motivo = form.cleaned_data.get('motivo')
        form.instance._change_reason = motivo
        form.instance.updated_by = self.request.user
        messages.success(self.request, "Paciente actualizado correctamente !!")
        return super().form_valid(form)
    

    def form_invalid(self, form):
        messages.error(self.request, "No se ha podido actualizar el Paciente")
        return super().form_invalid(form)


# view encargada de ejecutar la logica para eliminar un objeto del modelo
class EliminarGestacionView(MatronaRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Gestacion
    template_name = "confirmar_eliminacion.html"
    permission_required ="pacientes.delete_gestacion"
    raise_exception = True
    success_url = reverse_lazy("paciente:listar_gestaciones")
    form_class = MotivoForm


    def form_valid(self, form):
        messages.success(self.request, "Paciente eliminado correctamente !!")
        motivo = form.cleaned_data.get('motivo')
        self.object._change_reason = motivo
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, "No se pudo eliminar correctamente el objeto")
        return super().form_invalid(form)


# View de autocompletado para el formulario de gestacion
class AutoCompletadoDePaciente(MatronaRequiredMixin, autocomplete.Select2QuerySetView):
    # Esta view en cada input o change que se detecte el formulario en el navegador recibira ese valor y ejecutara la logica
    # del metodo get_queryset para ir autocompletando al usuario con el resultado o queryset que regrese este metodo.
    def get_queryset(self):
        query = self.q
        pacientes = Paciente.objects.all()
        
        if query:
            # annotate permite añadirle a todos los objetos del queryset un nuevo campo o field temporal que solo dura en la ejecucion del codigo
            # que almacena el resultado de una operacion, en este caso el proceso de concatenar el nombre  y los apellidos de los paciente para luego filtrar por
            # ese nuevo field de nombre_completo
            pacientes = pacientes.annotate(nombre_completo=Concat('nombre', Value(' '), 'primer_apellido', Value(' '), 'segundo_apellido'))
            return pacientes.filter(Q(identificacion__startswith=query) | Q(nombre_completo__icontains=query))
        return pacientes.none()



