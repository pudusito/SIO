from django.views.generic import CreateView,  UpdateView
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from django.shortcuts import get_object_or_404

from core.mixins import MatronaRequiredMixin
from ..forms import PuerperioForm
from ..models import Puerperio, Parto



class CreatePuerperioView(MatronaRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Puerperio
    form_class = PuerperioForm
    template_name = 'partos/formulario_puerperio.html'
    permission_required = 'partos.add_puerperio'
    raise_exception = True
    
    
    def form_valid(self, form):
        parto = get_object_or_404(Parto, pk=self.kwargs.get('pk_parto'))
        form.instance.created_by = self.request.user
        form.instance.updated_by = self.request.user
        form.instance.parto = parto
        messages.success(self.request, "Puerperio añadido al parto exitosamente")
        return super().form_valid(form)


    def get_success_url(self):
        return reverse('parto:detalles_parto', kwargs={'pk': self.kwargs.get('pk_parto')})
    


class UpdatePuerperioView(MatronaRequiredMixin, UpdateView):
    model = Puerperio
    form_class = PuerperioForm
    template_name = 'partos/formulario_puerperio.html'

    
    
    def form_valid(self, form):
        form.instance.updated_by = self.request.user
        messages.success(self.request, "Puerperio actualizado exitosamente")
        return super().form_valid(form)


    def get_success_url(self):
        return reverse('parto:detalles_parto', kwargs={'pk': self.kwargs.get('pk_parto')})