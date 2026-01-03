from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse
from django.conf import settings
from django.contrib import messages
from ..forms import ModificarPasswordForm

class ModificarPasswordView(LoginRequiredMixin, View):
    template_name = 'perfiles/modificar_password.html'
    form_class = ModificarPasswordForm
    success_url = None

    # Este se encarga de obtener el formulario vacio si es GET y si es POST le carga los datos
    # enviados desde el navegador
    def get_form(self, data=None):
        return self.form_class(data)

    # Metodo que ejecuta toda la logica o encapsula la logica si el formulario es valido
    def form_valid(self, form):
        user = self.request.user
        user.set_password(form.cleaned_data.get('new_password'))
        user.first_login = False
        user.save()
        messages.success(self.request, 'Contraseña actualizada correctamente')
        return redirect(self.get_success_url())

    # Metodo que ejecuta toda la logica o encapsula la logica si el formulario es invalido
    def form_invalid(self, form):
        messages.error(self.request, 'Error al actualizar contraseña')
        return self.render_response(form=form)

    # Se encarga de renderizar el template y manda todo los keyword que se le pasen a este
    def render_response(self, **kwargs):
        return render(self.request, self.template_name, kwargs)

    # Se encarga de obtener la url que deberia redireccionarse si se cambia correctamente 
    def get_success_url(self):
        if self.success_url is not None:
            return self.success_url
        return reverse(settings.LOGIN_URL)

    # si se envia un request tipo GET a la view se ejecuta esto
    def get(self, request, *args, **kwargs):
        form = self.get_form()
        return self.render_response(form=form)
    

    # si se envia un request tipo POST a la view se ejecuta esto
    # POST se reciben datos ya
    def post(self, request, *args, **kwargs):
        form = self.get_form(data=request.POST)
        if form.is_valid():
            return self.form_valid(form)
        
        return self.form_invalid(form)


