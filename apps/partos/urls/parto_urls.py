from django.urls import path

from ..views import (ListarPartosView, CrearPartosView, 
                     AutoCompletadoParaGestacion, MenuInicioPartosView, 
                     ActualizarPartoView, EliminarPartoView, WizardFormView,
                     CreatePuerperioView, DetallesPartoView, UpdatePuerperioView)

app_name = "parto"

urlpatterns = [
    path('', MenuInicioPartosView.as_view(), name="inicio"),
    path('listar/', ListarPartosView.as_view(), name="listar_partos"),
    path('agregar/', CrearPartosView.as_view(), name="agregar_parto"),
    path('<int:pk>/actualizar/', ActualizarPartoView.as_view(), name="actualizar_parto"),
    path('<int:pk>/eliminar/', EliminarPartoView.as_view(), name="eliminar_parto"),
    path('autocompletado/gestacion/', AutoCompletadoParaGestacion.as_view(), name="autocompletar_gestacion"),
    path('<int:pk>/detalles/', DetallesPartoView.as_view(), name="detalles_parto"),
    # puerperio
    path('<int:pk_parto>/add/puerperio/', CreatePuerperioView.as_view(), name="agregar_puerperio"),
    path('<int:pk_parto>/actualizar/puerperio/<int:pk>', UpdatePuerperioView.as_view(), name="actualizar_puerperio"),

    # wizard_url
    path('wizard-form/', WizardFormView.as_view(), name="wizard_form"),
]


