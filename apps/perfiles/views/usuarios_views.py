from django.views.generic import CreateView, ListView
from django.contrib.auth import get_user_model
from django.conf import settings
from django.urls import reverse_lazy
from django.core.mail import send_mail

from core.mixins import AdminTiRequiredMixin 
from core.utils import generar_password_aleatoria


class ListarUsuarios(AdminTiRequiredMixin, ListView):
    template_name = "perfiles/listar_usuarios.html"
    model = get_user_model()
    context_object_name = "usuarios"
    paginate_by = 10

class RegistrarUsuarioView(AdminTiRequiredMixin, CreateView):
    template_name = "perfiles/registrar_usuario.html"
    model = get_user_model()
    fields = ['username', 'email', 'first_name', 'last_name', 'es_matrona', 'es_supervisor']
    success_url = reverse_lazy("pantalla_principal")


    def form_valid(self, form):
        generate_password = generar_password_aleatoria()
        form.instance.set_password(generate_password)
        send_mail('Credenciales de Nuevo Usuario SIO', 
        f""" Se ha creado un usuario en el Sistema SIO para este correo 
        Estas son sus credenciales:
        <b>Correo:</b>{form.instance.email}
        <b>Password:</b> {generate_password}
        Estas credenciales son secretas nadie mas tiene acceso a ellas, asi que cuidelas y procure
        modificar la contraseña al momento de iniciar sesion por una que le apetezca.
        """, settings.DEFAULT_FROM_EMAIL, recipient_list=[form.instance.email])
        return super().form_valid(form)
    