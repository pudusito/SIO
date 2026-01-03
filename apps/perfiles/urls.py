from django.urls import path

from apps.perfiles.views.usuarios_views import ListarUsuarios
from .views import ModificarPasswordView, VerificarCodigoPorEmailView, RegistrarUsuarioView

app_name = "perfiles"

urlpatterns = [
    path('modificar-password/', ModificarPasswordView.as_view(), name='modificar_password'),
    path('verificacion-email/', VerificarCodigoPorEmailView.as_view(), name="verificar_codigo_email"),
    # Usuarios
    path('crear-usuario/', RegistrarUsuarioView.as_view(), name="crear_usuario"),
    path('listar-usuarios/', ListarUsuarios.as_view(), name='listar_usuarios'),
]
