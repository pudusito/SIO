from django.urls import path
from ..views import ActualizarPacienteView, CrearPacienteView, DetallePacienteView, EliminarPacienteView, MenuInicioPacienteView, ListarPacientesView

app_name = "paciente"


urlpatterns = [
    path('', MenuInicioPacienteView.as_view(), name="inicio"),
    path('listar/', ListarPacientesView.as_view(), name="listar_pacientes"),
    path('<int:pk>/detalle/', DetallePacienteView.as_view(), name="detalle_paciente"),
    path('agregar/', CrearPacienteView.as_view(), name="agregar_paciente"),
    path('<int:pk>/actualizar/', ActualizarPacienteView.as_view(), name="actualizar_paciente"),
    path('<int:pk>/eliminar/', EliminarPacienteView.as_view(), name="eliminar_paciente"),
]
