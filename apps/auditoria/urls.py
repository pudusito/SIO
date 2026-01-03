from django.urls import path
from . import views

app_name = "auditoria"


urlpatterns = [
    path('', views.MenuInicioAuditoriaView.as_view(), name="inicio"),
    path('actualizacion/<str:model_name>/detalle/<int:history_id>/', views.DetallesHistoricoActualizacionView.as_view(), name="historico_actualizacion"),
    path('eliminacion/<str:model_name>/detalle/<int:history_id>/', views.DetallesHistoricoEliminacionView.as_view(), name="historico_eliminacion"),
    path('creacion/<str:model_name>/detalle/<int:history_id>/', views.DetallesHistoricoCreacionView.as_view(), name="historico_creacion"),
    path('restaurar/<str:model_name>/registro/<int:history_id>/', views.RestauracionDeObjetoView.as_view(), name="restaurar_objeto"),
    
    # pacientes audit
    path('pacientes/', views.ListarHistoricoPaciente.as_view(), name="historicos_pacientes"),
    # path('paciente/<int:id_paciente>/historico/<str:tipo>/<int:pk>', views.CargarInfoHistoricoPacienteView.as_view(), name="historico_paciente"),
    # gestaciones audit
    path('gestaciones/', views.ListarHistoricoGestaciones.as_view(), name="historicos_gestaciones"),
    # partos audit
    path('partos/', views.ListarHistoricoPartos.as_view(), name="historicos_partos"),
    # recien nacidos audit
    path('rns/', views.ListarHistoricoRecienNacidos.as_view(), name="historicos_recien_nacidos")


]
