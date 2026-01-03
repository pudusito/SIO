from django.views.generic import TemplateView, ListView, View, DetailView, FormView
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.urls import reverse_lazy



from core.forms import MotivoForm
from core.mixins import SupervisorRequiredMixin
from .config import Gestacion, Paciente, Parto, RecienNacido, DeterminarModeloAuditarMixin, MODELOS_AUDITADOS





class MenuInicioAuditoriaView(SupervisorRequiredMixin,TemplateView):
    template_name = "auditoria/inicio_auditoria.html"



class ListarHistoricoPaciente(SupervisorRequiredMixin, ListView):
    model = Paciente
    template_name = "auditoria/historicos_pacientes.html"
    context_object_name = "historicos"
    paginate_by = 20

    def get_queryset(self):
        qs = Paciente.history.all().select_related('history_user')

        query_params = self.request.GET.copy()
        if 'page' in query_params:
            query_params.pop('page')

        self.query_string = query_params.urlencode()

        self.username = self.request.GET.get('username', "")
        self.start_date = self.request.GET.get('start_date', "")
        self.end_date = self.request.GET.get('end_date', "")
        self.tipo = self.request.GET.get('tipo', "")

        if self.username:
            qs = qs.filter(history_user__username=self.username)

        if self.start_date:
            qs = qs.filter(history_date__date__gte=self.start_date)
            # IMPORTANTE USAR el lookup __date para que compare la fecha simplemente si el campo es datetimefield si no pasara nuestra fecha a un datetime 
            # con 00:00 horas y evaluara que sea mayor e igual pero no solo de la fecha si no tmb por su hora 00:00

        if self.end_date:
            qs = qs.filter(history_date__date__lte=self.end_date)
        
        if self.tipo:
            qs = qs.filter(history_type=self.tipo)

        return qs.order_by('-history_date')


    def get_context_data(self, **kwargs):
        context_data =  super().get_context_data(**kwargs)
        context_data['username'] = self.username
        context_data['start_date'] = self.start_date
        context_data['end_date'] = self.end_date
        context_data['query_string'] = self.query_string
        context_data['tipo'] = self.tipo
        return context_data
    

class ListarHistoricoGestaciones(SupervisorRequiredMixin, ListView):
    model = Gestacion
    template_name = "auditoria/historicos_gestaciones.html"
    context_object_name = "historicos"
    paginate_by = 20

    def get_queryset(self):
        qs = Gestacion.history.all().select_related('history_user')

        query_params = self.request.GET.copy()
        if 'page' in query_params:
            query_params.pop('page')

        self.query_string = query_params.urlencode()

        self.username = self.request.GET.get('username', "")
        self.start_date = self.request.GET.get('start_date', "")
        self.end_date = self.request.GET.get('end_date', "")
        self.tipo = self.request.GET.get('tipo', "")

        if self.username:
            qs = qs.filter(history_user__username=self.username)

        if self.start_date:
            qs = qs.filter(history_date__date__gte=self.start_date)
            # IMPORTANTE USAR el lookup __date para que compare la fecha simplemente si el campo es datetimefield si no pasara nuestra fecha a un datetime 
            # con 00:00 horas y evaluara que sea mayor e igual pero no solo de la fecha si no tmb por su hora 00:00

        if self.end_date:
            qs = qs.filter(history_date__date__lte=self.end_date)
        
        if self.tipo:
            qs = qs.filter(history_type=self.tipo)

        return qs.order_by('-history_date')


    def get_context_data(self, **kwargs):
        context_data =  super().get_context_data(**kwargs)
        context_data['username'] = self.username
        context_data['start_date'] = self.start_date
        context_data['end_date'] = self.end_date
        context_data['query_string'] = self.query_string
        context_data['tipo'] = self.tipo
        return context_data
    


class ListarHistoricoPartos(SupervisorRequiredMixin, ListView):
    model = Parto
    template_name = "auditoria/historicos_partos.html"
    context_object_name = "historicos"
    paginate_by = 20

    def get_queryset(self):
        qs = Parto.history.all().select_related('history_user')

        query_params = self.request.GET.copy()
        if 'page' in query_params:
            query_params.pop('page')

        self.query_string = query_params.urlencode()

        self.username = self.request.GET.get('username', "")
        self.start_date = self.request.GET.get('start_date', "")
        self.end_date = self.request.GET.get('end_date', "")
        self.tipo = self.request.GET.get('tipo', "")

        if self.username:
            qs = qs.filter(history_user__username=self.username)

        if self.start_date:
            qs = qs.filter(history_date__date__gte=self.start_date)
            # IMPORTANTE USAR el lookup __date para que compare la fecha simplemente si el campo es datetimefield si no pasara nuestra fecha a un datetime 
            # con 00:00 horas y evaluara que sea mayor e igual pero no solo de la fecha si no tmb por su hora 00:00

        if self.end_date:
            qs = qs.filter(history_date__date__lte=self.end_date)
        
        if self.tipo:
            qs = qs.filter(history_type=self.tipo)

        return qs.order_by('-history_date')


    def get_context_data(self, **kwargs):
        context_data =  super().get_context_data(**kwargs)
        context_data['username'] = self.username
        context_data['start_date'] = self.start_date
        context_data['end_date'] = self.end_date
        context_data['query_string'] = self.query_string
        context_data['tipo'] = self.tipo
        return context_data
    
class ListarHistoricoRecienNacidos(SupervisorRequiredMixin, ListView):
    model = RecienNacido
    template_name = "auditoria/historicos_rn.html"
    context_object_name = "historicos"
    paginate_by = 20

    def get_queryset(self):
        qs = RecienNacido.history.all().select_related('history_user')

        query_params = self.request.GET.copy()
        if 'page' in query_params:
            query_params.pop('page')

        self.query_string = query_params.urlencode()

        self.username = self.request.GET.get('username', "")
        self.start_date = self.request.GET.get('start_date', "")
        self.end_date = self.request.GET.get('end_date', "")
        self.tipo = self.request.GET.get('tipo', "")

        if self.username:
            qs = qs.filter(history_user__username=self.username)

        if self.start_date:
            qs = qs.filter(history_date__date__gte=self.start_date)
            # IMPORTANTE USAR el lookup __date para que compare la fecha simplemente si el campo es datetimefield si no pasara nuestra fecha a un datetime 
            # con 00:00 horas y evaluara que sea mayor e igual pero no solo de la fecha si no tmb por su hora 00:00

        if self.end_date:
            qs = qs.filter(history_date__date__lte=self.end_date)
        
        if self.tipo:
            qs = qs.filter(history_type=self.tipo)

        return qs.order_by('-history_date')


    def get_context_data(self, **kwargs):
        context_data =  super().get_context_data(**kwargs)
        context_data['username'] = self.username
        context_data['start_date'] = self.start_date
        context_data['end_date'] = self.end_date
        context_data['query_string'] = self.query_string
        context_data['tipo'] = self.tipo
        return context_data
    


class DetallesHistoricoActualizacionView(SupervisorRequiredMixin, DeterminarModeloAuditarMixin, DetailView):
    model = ""
    template_name = "auditoria/detalles_auditoria_actualizacion.html"


    slug_url_kwarg = 'history_id'
    slug_field = 'history_id'

    def get_queryset(self):
        return self.model.history.select_related('history_user')


    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        prev_record_object = self.object.prev_record
        delta = self.object.diff_against(prev_record_object)
        context_data['delta'] = delta
        context_data['model_name'] = self.modelo_a_auditar._meta.model_name
        return context_data


class DetallesHistoricoEliminacionView(SupervisorRequiredMixin, DeterminarModeloAuditarMixin, DetailView):
    model = ""
    template_name = "auditoria/detalles_auditoria_eliminacion.html"


    slug_url_kwarg = 'history_id'
    slug_field = 'history_id'


    def get_queryset(self):
        return self.model.history.select_related('history_user')

    
    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['model_name'] = self.modelo_a_auditar._meta.model_name
        context_data['fields_to_display'] = self.fields_to_display().items()
        return context_data
    

    def fields_to_display(self):

        instance_field = dict()
        fields_to_hide = ['history_id', 'history_user', 'history_change_reason', 'history_date', 'history_type', 'updated_by']
        
        for field in self.object._meta.fields:
            try:
                if field.name in fields_to_hide:
                    continue
                instance_field[field.name] = getattr(self.object, field.name)
            except ObjectDoesNotExist:
                instance_field[field.name] = getattr(self.object, field.attname)
        
        return instance_field


class DetallesHistoricoCreacionView(DetallesHistoricoEliminacionView):
    template_name = "auditoria/detalles_auditoria_creacion.html"


class RestauracionDeObjetoView(SupervisorRequiredMixin, FormView):
    template_name ="auditoria/confirmar_restauracion.html"
    form_class = MotivoForm
    model = ""
    success_url = reverse_lazy('auditoria:inicio')

    def dispatch(self, request, model_name = None, history_id = None, *args, **kwargs):
        self.model = MODELOS_AUDITADOS.get(model_name)
        if not self.model or not history_id:
            raise Http404()
        
        self.object = get_object_or_404(self.model.history.all(), history_id=history_id)
        return super().dispatch(request, *args, **kwargs)
    

    def form_valid(self, form):
        motivo = form.cleaned_data.get('motivo')
        try:
            recuperacion = self.object.instance
            recuperacion._change_reason = motivo
            recuperacion.save()
        except ObjectDoesNotExist:
            messages.error(self.request, "Fue imposible restaurar el objeto a esta version, porque ya no existe")

        # formview no almacena nada en el modelo, solo genera una redireccion a la success url
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context_data =  super().get_context_data(**kwargs)
        context_data['object'] = self.object
        return context_data


