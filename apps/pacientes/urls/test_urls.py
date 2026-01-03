from django.urls import path
from ..views import CrearTestHepatitisBView, CrearTestVihView, CrearTestSgbView, CrearTestVdrlView

app_name = "test"

urlpatterns = [
    path('add/hepatitisb/', CrearTestHepatitisBView.as_view(), name="crear_test_hepatitisb"),
    path('add/vih/', CrearTestVihView.as_view(), name="crear_test_vih"),
    path('add/sgb/', CrearTestSgbView.as_view(), name="crear_test_sgb"),
    path('add/vdrl/', CrearTestVdrlView.as_view(), name="crear_test_vdrl")
]
