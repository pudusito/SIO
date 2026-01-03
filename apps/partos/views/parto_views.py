from django.views.generic import ListView, CreateView, TemplateView, UpdateView, DeleteView, DetailView
from django.contrib.auth.mixins import PermissionRequiredMixin
from dal import autocomplete
from django.db.models import Q, Value, F
from django.db.models.functions import Concat
from django.urls import reverse_lazy
from django.contrib import messages

from core.forms import MotivoForm
from core.mixins import MatronaSupervisorRequiredMixin, MatronaRequiredMixin
from ..models import Parto
from apps.pacientes.models import Gestacion
from ..forms import PartoForm



class MenuInicioPartosView(MatronaSupervisorRequiredMixin, TemplateView):
    template_name = "partos/inicio_partos.html"


class ListarPartosView(MatronaSupervisorRequiredMixin, PermissionRequiredMixin, ListView):
    model = Parto
    template_name = "partos/listar_partos.html"
    permission_required = "partos.view_parto"
    raise_exception = True
    context_object_name = "partos"


    def get_queryset(self):
        qs =  self.model.objects.select_related('gestacion__paciente', 'via_nacimiento')
        qs = qs.annotate(nombre_completo_paciente=Concat('gestacion__paciente__nombre', Value(' '), 'gestacion__paciente__primer_apellido', Value(' '), 'gestacion__paciente__segundo_apellido'))
        query_params = self.request.GET.copy()
        if 'page' in query_params:
            query_params.pop('page')

        self.query_string = query_params.urlencode()

        self.query = self.request.GET.get('query')


        if self.query and '.' in self.query:
            self.query = self.query.replace('.', '')


        if self.query:
            qs = qs.filter(Q(nombre_completo_paciente__icontains=self.query) | Q(gestacion__paciente__identificacion__startswith=self.query))


            
        return qs.order_by('-created_at')

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context['query_string'] = self.query_string
        context['query'] = self.query
        return context

class DetallesPartoView(MatronaSupervisorRequiredMixin, DetailView):
    model = Parto
    template_name = "partos/detalles_parto.html"
    


class CrearPartosView(MatronaRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Parto
    template_name = "partos/formulario_parto.html"
    permission_required = "partos.add_parto"
    raise_exception = True
    form_class = PartoForm
    success_url = reverse_lazy("parto:listar_partos")

    def form_valid(self, form):
        form.instance.gestacion.estado = "terminada"
        form.instance.created_by = self.request.user
        form.instance.updated_by = self.request.user
        messages.success(self.request, "Parto creado exitosamente !!")
        return super().form_valid(form)
    

    def form_invalid(self, form):
        messages.error(self.request, "No se pudo registrar el parto !!")
        return super().form_invalid(form)
        
    
    


# view encargada se ejecutar la logica para actualizar los datos de un paciente
class ActualizarPartoView(MatronaRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Parto
    template_name = "partos/formulario_parto.html"
    form_class = PartoForm
    permission_required= "partos.change_parto"
    raise_exception = True
    context_object_name = "parto"
    success_url = reverse_lazy("parto:listar_partos")

    def form_valid(self, form):
        motivo = form.cleaned_data.get('motivo')
        form.instance._change_reason = motivo
        form.instance.updated_by = self.request.user
        messages.success(self.request, "Parto actualizado correctamente !!")
        return super().form_valid(form)
    

    def form_invalid(self, form):
        messages.error(self.request, "No se ha podido actualizar el parto !!")
        return super().form_invalid(form)


# view encargada de ejecutar la logica para eliminar un objeto del modelo
class EliminarPartoView(MatronaRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Parto
    template_name = "confirmar_eliminacion.html"
    permission_required ="partos.delete_parto"
    raise_exception = True
    success_url = reverse_lazy("parto:listar_partos")
    form_class = MotivoForm


    def form_valid(self, form):
        messages.success(self.request, "Parto eliminado correctamente !!")
        motivo = form.cleaned_data.get('motivo')
        self.object._change_reason = motivo
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, "No se pudo eliminar correctamente el objeto")
        return super().form_invalid(form)


# View para autocompletar la busqueda del formulario Partos para el campo gestacion/gestaciones
class AutoCompletadoParaGestacion(MatronaRequiredMixin, autocomplete.Select2QuerySetView):
    def get_queryset(self):
        gestaciones = Gestacion.objects.all()
        

        if self.q:
            gestaciones = gestaciones.annotate(nombre_completo_paciente=Concat('paciente__nombre', Value(' '), 'paciente__primer_apellido', Value(' '), 'paciente__segundo_apellido'), 
                                               identificacion_paciente=F('paciente__identificacion'))
            # Aqui igual puede ser: paciente__identificacion__startswith=self.q
            return gestaciones.filter(Q(nombre_completo_paciente__icontains=self.q) | Q(identificacion_paciente__startswith=self.q) | Q(pk__startswith=self.q)).order_by('nombre_completo_paciente')
        return gestaciones.none()