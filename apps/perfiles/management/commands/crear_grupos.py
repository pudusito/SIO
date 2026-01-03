from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from apps.pacientes.models import Gestacion, Paciente, TestHepatitisB, TestVdrl, TestVih, TestSgb
from apps.partos.models import AnalgesiaParto, Puerperio, Profesional, Participacion, Parto
from apps.recien_nacidos.models import RecienNacido, Vacunacion
from apps.perfiles.models import MatronaPerfil, SupervisorPerfil, Turno, Usuario




# Nuestro propio comando de django que puede ejecutar luego el manage.py igual como lo hace con los comandos
# showmigrations, makemigrations, shell, runserver, migrate, que son solo archivos que implementan una clase Command
# que hereda de BaseCommand, django podra ejecutar el manage.py cualquier clase Command que Herede de BaseCommand como comando
class Command(BaseCommand):
    help = "Crea los grupos principales y les asigna permisos"

    GENERAR_CRUD = ["add", "view", "change", "delete"]

    DEFINICION_REGLAS = {
        # cada key del diccionario es un grupo que crearemos y asociaremos los permisos que configuremos en la lista que le asignamos
        'Matrona': [
            # Cada tupla es una regla de permisos para ese modelo que tendra el grupo, en este caso Matrona
            (Paciente, ['all']),
            (Parto, ['all']),
            (Gestacion, ['all']),
            (TestHepatitisB, ['all']),
            (TestVdrl, ['all']),
            (TestVih, ['all']),
            (TestSgb, ['all']),
            (AnalgesiaParto, ['all']),
            (Puerperio, ['all']),
            (Profesional, ['all']),
            (Participacion, ['all']),
            (RecienNacido, ['all']),
            (Vacunacion, ['all']),
            (MatronaPerfil, ['view', 'change']),
            (Usuario, ['view', 'change']),
        ],
        'Supervisor': [
            (Paciente, ['view']),
            (Parto, ['view']),
            (Gestacion, ['view']),
            (TestHepatitisB, ['view']),
            (TestVdrl, ['view']),
            (TestVih, ['view']),
            (TestSgb, ['view']),
            (AnalgesiaParto, ['view']),
            (Puerperio, ['view']),
            (Profesional, ['view']),
            (Participacion, ['view']),
            (RecienNacido, ['view']),
            (Vacunacion, ['view', 'view_no_existo']),
            (Turno, ['all']),
            (SupervisorPerfil, ['view', 'change']),
            (Usuario, ['view', 'change']),
        ],
        'AdminTi': [
            (Usuario, ['view', 'add', 'change']),
        ],
    }

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING("Asegurate de haber realizado las migraciones correspondientes. Desea continuar ? [y/n]: "))
        confirmacion = input("respuesta: ")
        if confirmacion.lower() == 'y':
            for nombre_grupo, reglas in self.DEFINICION_REGLAS.items():
                grupo, _ = Group.objects.get_or_create(name=nombre_grupo)

                permisos_asignar = set()  # evita duplicados

                for modelo, permisos in reglas:
                    content_type = ContentType.objects.get_for_model(modelo)

                    for permiso in permisos:
                        if permiso == 'all':
                            # Genera CRUD explícitamente
                            for accion in self.GENERAR_CRUD:
                                codename = f"{accion}_{modelo._meta.model_name}"
                                try:
                                    p = Permission.objects.get(
                                        codename=codename,
                                        content_type=content_type
                                    )
                                    permisos_asignar.add(p)
                                except Permission.DoesNotExist:
                                    self.stdout.write(self.style.ERROR(
                                    f"ERROR CRÍTICO: No se encontró el permiso '{codename}'."
                                    ))
                                    self.stdout.write(self.style.WARNING(
                                        f"  -> PISTA: ¿Ejecutaste 'python manage.py migrate'? "
                                        f"Los permisos estándar se crean automáticamente tras la migración."
                                    ))

                        else:
                            # Permisos específicos ("view", "change", etc)
                            codename = f"{permiso}_{modelo._meta.model_name}"
                            try:
                                p = Permission.objects.get(
                                    codename=codename,
                                    content_type=content_type
                                )
                                permisos_asignar.add(p)
                            except Permission.DoesNotExist:
                                self.stdout.write(self.style.ERROR(f"El permiso {codename} no existe. Asi que no se aplico. Revise la configuracion del script"))

                grupo.permissions.set(permisos_asignar)
                self.stdout.write(self.style.SUCCESS(f"Grupo {nombre_grupo} actualizado."))
        else:
            self.stdout.write(self.style.WARNING("No se han aplicado cambios"))


