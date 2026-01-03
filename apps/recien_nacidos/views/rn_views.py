from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView
from django.contrib.auth.mixins import PermissionRequiredMixin
from dal import autocomplete
from django.db.models.functions import Concat
from django.db.models import Value, Q, F

from ..forms import RecienNacidoForm
from ..models import RecienNacido
from apps.partos.models import Parto
from core.mixins import MatronaRequiredMixin, MatronaSupervisorRequiredMixin
from core.forms import MotivoForm

class MenuInicioRecienNacido(MatronaSupervisorRequiredMixin, TemplateView):
    template_name = "recien_nacidos/inicio_rn.html"


class ListarRecienNacidoView(MatronaSupervisorRequiredMixin, PermissionRequiredMixin, ListView):
    model = RecienNacido
    template_name = "recien_nacidos/listar_rn.html"
    context_object_name = "recien_nacidos"
    raise_exception = True
    permission_required = "recien_nacidos.view_reciennacido"

    def get_queryset(self):
        return self.model.objects.select_related('parto__gestacion__paciente')



class CrearRecienNacidoView(MatronaRequiredMixin, PermissionRequiredMixin, CreateView):
    model = RecienNacido
    template_name = "recien_nacidos/formulario_rn.html"
    form_class = RecienNacidoForm
    permission_required = "recien_nacidos.add_reciennacido"
    raise_exception = True
    success_url = reverse_lazy('recien_nacido:listar_recien_nacidos')


    def form_valid(self, form):
        form.instance.parto.estado = "terminado"
        form.instance.created_by = self.request.user
        form.instance.updated_by = self.request.user
        return super().form_valid(form)



# view encargada se ejecutar la logica para actualizar los datos de un paciente
class ActualizarRecienNacidoView(MatronaRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = RecienNacido
    template_name = "partos/formulario_parto.html"
    form_class = RecienNacidoForm
    permission_required= "recien_nacidos.change_reciennacido"
    raise_exception = True
    context_object_name = "recien_nacido"
    success_url = reverse_lazy("recien_nacido:listar_recien_nacidos")

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
class EliminarRecienNacidoView(MatronaRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = RecienNacido
    template_name = "confirmar_eliminacion.html"
    permission_required ="recien_nacidos.delete_reciennacido"
    raise_exception = True
    success_url = reverse_lazy("recien_nacido:listar_recien_nacidos")
    form_class = MotivoForm


    def form_valid(self, form):
        messages.success(self.request, "Paciente eliminado correctamente !!")
        motivo = form.cleaned_data.get('motivo')
        self.object._change_reason = motivo
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, "No se pudo eliminar correctamente el objeto")
        return super().form_invalid(form)


class AutoCompletadoDePartosView(MatronaRequiredMixin, autocomplete.Select2QuerySetView):
    def get_queryset(self):
        partos = Parto.objects.all()

        if self.q:
            partos = partos.annotate(nombre_completo_paciente=Concat('gestacion__paciente__nombre', Value(' '), 'gestacion__paciente__primer_apellido', Value(' '), 'gestacion__paciente__segundo_apellido'),
                                     identificacion_paciente=F('gestacion__paciente__identificacion'))
            
            return partos.filter(Q(nombre_completo_paciente__icontains=self.q) | Q(identificacion_paciente__startswith=self.q) | Q(pk__startswith=self.q))
        
        return partos.none()