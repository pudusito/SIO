from django.conf import settings
from django.shortcuts import redirect
from django.urls import reverse_lazy

# Para los que vean este codigo un middleware es una clase que luego se ejecuta como una funcion, si quieren que los objetos
# de una clase se ejecuten como funciones y ejecuten alguna tarea deben implementarle el metodo __call__
class FirstLoginMiddleware:
    
    redirect_url = reverse_lazy("perfiles:modificar_password")

    def __init__(self, get_response):
        self.get_response = get_response


    def __call__(self, request):
        if request.user.is_authenticated and request.user.first_login and not any(request.path.startswith(path) 
                                                                                  for path in settings.PUBLIC_URLS):
            return redirect(self.redirect_url)


        return self.get_response(request)