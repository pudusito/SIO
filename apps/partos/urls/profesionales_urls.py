from django.urls import path
# Importamos las vistas desde tu carpeta views
from ..views import ListarProfesionalesView, CrearProfesionalView, MenuInicioProfesionalesView, CrearParticipacion
# LE DAMOS SU PROPIO NOMBRE DE APP (NAMESPACE)
app_name = "profesionales"

urlpatterns = [

    path('', MenuInicioProfesionalesView.as_view(), name="inicio"),
    path('listar/', ListarProfesionalesView.as_view(), name="listar"),
    path('agregar/', CrearProfesionalView.as_view(), name="agregar"),
    path('<int:parto_id>/add/participacion', CrearParticipacion.as_view(), name="agregar_participacion")

]