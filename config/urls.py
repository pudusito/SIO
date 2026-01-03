# ROOT CONF URL
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import LogoutView
from django.conf import settings

from apps.perfiles.views import LoginView, MostrarPantallaPrincipalView


urlpatterns = [
    path('', MostrarPantallaPrincipalView.as_view(), name="pantalla_principal"),
    path('admin/', admin.site.urls),
    path('login/', LoginView.as_view(), name="login"),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('pacientes/', include('apps.pacientes.urls.paciente_urls')),
    path('gestaciones/', include('apps.pacientes.urls.gestacion_urls')),
    path('tests/', include('apps.pacientes.urls.test_urls')),
    path('partos/', include('apps.partos.urls.parto_urls')),
    path('perfiles/', include('apps.perfiles.urls')),
    path('rn/', include('apps.recien_nacidos.urls.rn_urls')),
    path('reportes/', include('apps.reportes.urls')),
    path('auditorias/', include('apps.auditoria.urls')),
    path('dashboards/', include('apps.dashboard.urls')),
    path('profesionales/', include('apps.partos.urls.profesionales_urls')),    
]

if settings.DEBUG:
    from django.shortcuts import render

    def probar_errores(request):
        return render(request, '403.html', status=404)

    def tailwind_testear(request):
        return render(request, 'tailwindsito.html')

    urlpatterns += [
        path('tailwind/', tailwind_testear),
        path('403/', probar_errores, name='error_404')
    ]


