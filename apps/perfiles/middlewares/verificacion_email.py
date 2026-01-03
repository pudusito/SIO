# Middleware encargado de validar si el usuario esta verificado por un codigo enviado al email
# si es asi entonces puede pasar sus request o solicitudes a las view o funcionalidades que necesite
# si no se redirige a la view que genera el codigo y procesa el codigo y se encarga de verificar su session


from django.shortcuts import redirect
from django.conf import settings

class VerificacionEmailMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response


    def __call__(self, request, *args, **kwds):
        if request.user.is_authenticated and not request.user.first_login and not any(request.path.startswith(path) for path in settings.PUBLIC_URLS):
            if request.session.get('verificado', None):
                return self.get_response(request)
            return redirect("perfiles:verificar_codigo_email")
        
        return self.get_response(request)
    

