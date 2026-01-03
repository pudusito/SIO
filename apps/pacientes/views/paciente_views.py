from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.urls import reverse_lazy
from django.contrib import messages
from django.db.models import Q, Value
from django.db.models.functions import Concat
from django.contrib.auth.mixins import PermissionRequiredMixin
from core.mixins import MatronaRequiredMixin, SupervisorRequiredMixin, MatronaSupervisorRequiredMixin
from core.forms import MotivoForm
from ..forms import PacienteForm
from ..models import Paciente



class MenuInicioPacienteView(MatronaSupervisorRequiredMixin, TemplateView):
    template_name="pacientes/inicio_pacientes.html"


# View encargada de listar todos los pacientes al usuario que lo solicite
class ListarPacientesView(MatronaSupervisorRequiredMixin, PermissionRequiredMixin, ListView):
    model = Paciente
    permission_required = "pacientes.view_paciente"
    raise_exception = True
    template_name = 'pacientes/listar_pacientes.html'
    context_object_name = 'pacientes'
    paginate_by = 8    
    

    def get_queryset(self):
        # Por ahora se entregan todos los pacientes a todas las matronas, despues vemos si filtramos
        qs =  self.model.objects.select_related('tipo', 'comuna', 'nacionalidad')
        qs = qs.annotate(nombre_completo=Concat('nombre', Value(' '), 'primer_apellido', Value(' '), 'segundo_apellido'))
        
        # Aqui creamos el query string a partir de los parametros de query que se envian por la url para poder añadirlos en el template
        # en el paginador para seguir enviando los valores que el usuario proporcione
        query_params = self.request.GET.copy()
        if 'page' in query_params:
            query_params.pop('page')
        self.query_string = query_params.urlencode()
        
        # ahora aqui definimos que valores tomaremos realmente en serio de los que nos envie el cliente desde el navegador
        # ya que un usuario de cualquier web puede desde el navegador en la url enviar valores por GET en los queryparams pero solo el servidor
        # define que params son los que usara para filtrar, buscar algo o hacer lo que estime comveniente, en este caso nosotros lo usaremos para filtrar
        # los pacientes

        self.query = self.request.GET.get('query')

        self.plan_de_parto = self.request.GET.get('pp')
        



        # Cabros si se manda desde el navegador un params llamado query filtramos si no, no lo hacemos
        if self.query:
            qs = qs.filter(Q(nombre_completo__icontains=self.query) | Q(identificacion__startswith=self.query))

        return qs.order_by('-created_at')

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context['query_string'] = self.query_string
        context['query'] = self.query
        return context


# View encargada de mostrar los detalles de cada paciente
class DetallePacienteView(MatronaSupervisorRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Paciente
    permission_required = "pacientes.view_paciente"
    raise_exception = True
    template_name = 'pacientes/detalle_paciente.html'
    context_object_name = 'paciente'

    def get_queryset(self):
        qs = self.model.objects.select_related('tipo', 'comuna', 'nacionalidad', 'cesfam')
        return qs



# View para añadir o crear un nuevo Paciente en el servidor
class CrearPacienteView(MatronaRequiredMixin, CreateView):
    model = Paciente
    template_name = 'pacientes/formulario_paciente.html'
    form_class = PacienteForm
    success_url = reverse_lazy('paciente:listar_pacientes')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.updated_by = self.request.user
        messages.success(self.request, 'Paciente creado correctamente')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Error al registrar el paciente')
        return super().form_invalid(form
                                    )



# view encargada se ejecutar la logica para actualizar los datos de un paciente
class ActualizarPacienteView(MatronaRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Paciente
    template_name = "pacientes/formulario_paciente.html"
    form_class = PacienteForm
    permission_required= "pacientes.change_paciente"
    raise_exception = True
    context_object_name = "paciente"
    success_url = reverse_lazy("paciente:listar_pacientes")

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
class EliminarPacienteView(MatronaRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Paciente
    template_name = "confirmar_eliminacion.html"
    permission_required ="pacientes.delete_paciente"
    raise_exception = True
    success_url = reverse_lazy("paciente:listar_pacientes")
    form_class = MotivoForm


    def form_valid(self, form):
        messages.success(self.request, "Paciente eliminado correctamente !!")
        motivo = form.cleaned_data.get('motivo')
        self.object._change_reason = motivo
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, "No se pudo eliminar correctamente el objeto")
        return super().form_invalid(form)



