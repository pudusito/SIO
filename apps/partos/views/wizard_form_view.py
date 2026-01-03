from django.shortcuts import redirect
from formtools.wizard.views import SessionWizardView
from django.db import transaction
from django.contrib import messages


from ..forms import GestacionFormWizard, PacienteFormWizard, PartoFormWizard, RecienNacidoFormWizard
from ..forms import PuerperioForm as PuerperioFormWizard
from core.mixins import MatronaRequiredMixin

class WizardFormView(MatronaRequiredMixin, SessionWizardView):
    # pass in the orden that the user will process them.
    form_list = [PacienteFormWizard, GestacionFormWizard, PartoFormWizard, PuerperioFormWizard, RecienNacidoFormWizard]

    # specify the templates that the form wizards will use
    TEMPLATES = {
        '0': 'wizard/fields_paciente_form.html',
        '1': 'wizard/fields_gestacion_form.html',
        '2': 'wizard/fields_parto_form.html',
        '3': 'wizard/fields_puerperio_form.html',
        '4': 'wizard/fields_recien_nacido_form.html'
    }

    # Optionally specify a file_storage atributte  

    # the method to execute when all forms are valids
    def done(self, form_list, **kwargs):
        try:
            with transaction.atomic():
                # storage of patient
                patient = form_list[0].save(commit=False)
                patient.created_by = self.request.user
                patient.updated_by = self.request.user
                patient.save()

                # storage of gestation
                gestation = form_list[1].save(commit=False)
                gestation.paciente = patient
                gestation.created_by = self.request.user
                gestation.updated_by = self.request.user
                gestation.save()
                gestation.estado = "terminada"
                gestation.save()

                # storage of childbirth
                childbirth = form_list[2].save(commit=False)
                childbirth.gestacion = gestation
                childbirth.created_by = self.request.user
                childbirth.updated_by = self.request.user
                childbirth.save()
                childbirth.estado = "terminado"
                childbirth.save()


                # storage of puerperio
                puerperium = form_list[3].save(commit=False)
                puerperium.parto = childbirth
                puerperium.created_by = self.request.user
                puerperium.updated_by = self.request.user
                puerperium.save()

                # storage of baby
                baby = form_list[4].save(commit=False)
                baby.parto = childbirth
                baby.created_by = self.request.user
                baby.updated_by = self.request.user
                baby.save()
                messages.success(self.request, "Ingreso de datos realizado con exito")
                return redirect('pantalla_principal')
        except Exception as e:
            print(f"Error al guardar el wizard: {e}")
            messages.error(self.request, f"Error al guardar el wizard: {e}")
            return redirect('pantalla_principal')

    # Método OBLIGATORIO para que el diccionario de arriba funcione
    def get_template_names(self):
        return [self.TEMPLATES[self.steps.current]]
    
    