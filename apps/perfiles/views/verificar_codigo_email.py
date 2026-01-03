from random import randint
from datetime import timedelta
from django.views import View
from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from ..forms import CodigoVerificacionEmailForm
from ..models import CodigoVerificacionEmail

class VerificarCodigoPorEmailView(LoginRequiredMixin, View):
    '''
    View que se encarga de Generar el codigo que se envia al email del usuario por seguridad y 
    de validar que el usuario no tenga ya un codigo creado que no ha expirado si es asi se le dice que no puede generar uno nuevo
    hasta que pasen 3 minutos.
    Ademas tambien verifica que el codigo enviado este en el rango de 6 digitos con la validacion del formulari e igualmente que sea valido y 
    exista en la base de datos ese codigo asociado al usuario sin expirar para verificar su session.
    '''
    template_name = 'perfiles/verificar_codigo_email.html'
    form_class = CodigoVerificacionEmailForm

    def get_form(self, *args, **kwargs):
        return self.form_class(*args, **kwargs)


    def get(self, request):
        form = self.get_form()
        codigo = randint(100_000, 999_999)   
        tiempo_consulta = timezone.localtime(timezone.now())
        try:
            codigo_obj = CodigoVerificacionEmail.objects.create(
                user=request.user,
                code=codigo,
                expired_at=timezone.localtime(tiempo_consulta + timedelta(minutes=1))
            )
            send_mail(
                subject="Código Verificación",
                message=f"Tu código es {codigo}",
                recipient_list=[request.user.email],
                from_email=settings.DEFAULT_FROM_EMAIL
            )
            
            messages.success(request, "Se le ha generado código de verificacion. Revisa tu correo para saber tu código.")
            
            tiempo_restante = codigo_obj.expired_at - tiempo_consulta
            segundos_totales = int(tiempo_restante.total_seconds())
            minutos = segundos_totales // 60
            segundos = segundos_totales % 60
            messages.info(request, f"{minutos:02d}:{segundos:02d}")

        except IntegrityError:
            codigo_obj = CodigoVerificacionEmail.objects.get(user=request.user)
            if codigo_obj.expired_at < tiempo_consulta:
                codigo_obj.delete()
                return redirect('perfiles:verificar_codigo_email')
            tiempo_restante = codigo_obj.expired_at - tiempo_consulta
            segundos_totales = int(tiempo_restante.total_seconds())
            minutos = segundos_totales // 60
            segundos = segundos_totales % 60
            messages.warning(request, "Ya tienes un código generado.")
            messages.info(request, f"{minutos:02d}:{segundos:02d}")
        return render(request, self.template_name, {'form': form})


    def post(self, request):
        form = self.get_form(data=request.POST)
        tiempo_consulta = timezone.localtime(timezone.now())

        codigo_obj = CodigoVerificacionEmail.objects.filter(user=request.user).first()
        if not codigo_obj:
            messages.error(request, "No tienes un código generado. Solicita uno nuevo.")
            return render(request, self.template_name, {'form': form})

        if form.is_valid():
            codigo_validado = form.cleaned_data['codigo']

            if codigo_obj.code == codigo_validado and codigo_obj.expired_at > tiempo_consulta:
                # Aqui vericamos la session podra acceder a todas las funcionalidades que tenga permiso
                request.session['verificado'] = True
                codigo_obj.delete()
                messages.success(request, "Has inicado sesion correctamente")
                return redirect(settings.LOGIN_REDIRECT_URL)

        tiempo_restante = codigo_obj.expired_at - tiempo_consulta
        segundos_totales = int(tiempo_restante.total_seconds())

        if segundos_totales > 0:
            minutos = segundos_totales // 60
            segundos = segundos_totales % 60
            messages.info(request, f"{minutos:02d}:{segundos:02d}")
        else:
            messages.info(request, f"{0:02d}:{0:02d}")
            codigo_obj.delete()

        messages.error(request, "Código invalido o expirado. Intentalo nuevamente o Solicite uno nuevo.")

        return render(request, self.template_name, {'form': form})

    