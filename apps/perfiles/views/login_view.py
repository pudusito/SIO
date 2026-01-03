from django.contrib.auth.views import LoginView as BaseLoginView
from django.conf import settings
from ..forms import LoginEmailForm
from django.contrib import messages

# View encargada de manejar el proceso de login del usuario
class LoginView(BaseLoginView):
    authentication_form = LoginEmailForm

    # Este es para redireccionar al usuario si ya esta autenticado, por defecto se usa el REDIRECT_LOGIN_URL
    redirect_authenticated_user = True

    

    # Cargamos mensaje de error, para renderizar en el template del login.html cuando el formulario sea invalido
    # entonces este mensaje lo renderizaremos en el login junto a los datos del formulario
    def form_invalid(self, form):
        messages.error(self.request, 'Error al iniciar sesión, credenciales invalidas. Intente nuevamente')
        return super().form_invalid(form)
        
    
    def get_context_data(self, **kwargs):
        context_data =  super().get_context_data(**kwargs)
        context_data['DEBUG'] = settings.DEBUG
        return context_data