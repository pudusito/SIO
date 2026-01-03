# Import the most important forms from the wizard
from apps.pacientes.forms import GestacionForm, PacienteForm
from apps.partos.forms  import PartoForm
from apps.recien_nacidos.forms import RecienNacidoForm



class PacienteFormWizard(PacienteForm):
    pass


class GestacionFormWizard(GestacionForm):
    class Meta(GestacionForm.Meta):
        # Convert to a list to prevent it from being converted to a tuple 
        exclude = list(GestacionForm.Meta.exclude) + ['paciente']


class PartoFormWizard(PartoForm):
    class Meta(PartoForm.Meta):
        exclude = list(PartoForm.Meta.exclude) + ['gestacion']



class RecienNacidoFormWizard(RecienNacidoForm):
    class Meta(RecienNacidoForm.Meta):
        exclude = list(RecienNacidoForm.Meta.exclude) + ['parto']

