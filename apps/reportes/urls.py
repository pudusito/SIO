from django.urls import path
from .views import GenerarReporteCesarea, GenerarReporteCaracteristicasParto, GenerarReporteD1, GenerarReporteD2, GenerarReporteEsterilizacionesQuirurgicas, GenerarReporteEutocicoDistocico, GenerarReporteHepatitisB, GenerarReporteModeloAtencion, GenerarReporteProfilaxisGonorrea

from .views.inicio_views import inicio_reportes
from .views import parto_csv, paciente_csv

app_name = "reportes"

urlpatterns = [

    path('', inicio_reportes, name="inicio_reportes"),

    path('cesarea/', GenerarReporteCesarea.as_view(), name="crear_reporte_cesarea"),
    path('caract-parto/', GenerarReporteCaracteristicasParto.as_view(), name="crear_reporte_caracteristicas_parto"),
    path('d1/', GenerarReporteD1.as_view(), name="crear_reporte_d1"),
    path('d2/', GenerarReporteD2.as_view(), name ="crear_reporte_d2"),
    path('est-quirurgicas/', GenerarReporteEsterilizacionesQuirurgicas.as_view(), name="crear_reporte_esterilizaciones_quirurgicas"),
    path('eutocico-distocico/', GenerarReporteEutocicoDistocico.as_view(), name="crear_reporte_eutocico_distocico"),
    path('hepatitis-b/', GenerarReporteHepatitisB.as_view(), name="crear_reporte_hepatitis_b"),
    path('modelo-atencion/', GenerarReporteModeloAtencion.as_view(), name="crear_reporte_modelo_atencion"),
    path('profilaxis-gonorrea/', GenerarReporteProfilaxisGonorrea.as_view(), name="crear_reporte_profilaxis_gonorrea"),
    path('excel/parto', parto_csv, name="parto_csv"),
    path('excel/paciente', paciente_csv, name="paciente_csv")
]
