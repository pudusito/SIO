from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


# Mixin que exigira que se este autenticado y sea matrona para ejecutar la logica o funcionalidad
class MatronaRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.es_matrona



class SupervisorRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.es_supervisor



class AdminTiRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff



class MatronaSupervisorRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.es_matrona or self.request.user.es_supervisor