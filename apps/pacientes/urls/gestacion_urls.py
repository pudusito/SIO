from django.urls import path
from ..views import CrearGestacionView, ListarGestacionesView, AutoCompletadoDePaciente, MenuInicioGestacionesView, ActualizarGestacionView, EliminarGestacionView


app_name = "gestacion"


urlpatterns = [
    path('', MenuInicioGestacionesView.as_view(), name="inicio"),
    path('listar/', ListarGestacionesView.as_view(), name="listar_gestaciones"),
    path('agregar/', CrearGestacionView.as_view(), name="agregar_gestacion"),
    path('<int:pk>/actualizar/', ActualizarGestacionView.as_view(), name="actualizar_gestacion"),
    path('<int:pk>/eliminar/', EliminarGestacionView.as_view(), name="eliminar_gestacion"),
    path('autocomplete/paciente/', AutoCompletadoDePaciente.as_view(), name='autocompletar_paciente')
]
