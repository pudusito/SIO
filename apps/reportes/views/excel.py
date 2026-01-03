import csv
import codecs

from django.http import HttpResponse
from apps.pacientes.models import Paciente
from apps.partos.models import Parto


def paciente_csv(request):

    response = HttpResponse(
        content_type="text/csv; charset=utf-8",
        headers={"Content-Disposition": 'attachment; filename="reporte_pacientes.csv"'},
    )

    response.write(codecs.BOM_UTF8) 
    
    pacientes = Paciente.objects.select_related('tipo', 'cesfam', 'comuna', 'nacionalidad')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    if start_date:
        pacientes = pacientes.filter(created_at__gte=start_date)
    
    if end_date:
        pacientes = pacientes.filter(created_at__lte=end_date)
    
    writer = csv.writer(response) 

    print(start_date)
    print(end_date)
    
    writer.writerow([
        'Nombre', 'Apellido 1', 'Apellido 2', 'Sexo', 'Tipo Paciente', 'Nacionalidad',
        'Comuna', 'Cesfam', 'Direccion', 'Telefono', 'Tipo de Documento', 'NºDocumento',
        'Fecha de Nacimiento', 'Edad Paciente', 'Descapacitado', 'Pueblo Originario',
        'Privada de Libertad', 'Es Transexual', 'Plan de Parto', 'Visita Guiada', 'Peso',
        'Altura', 'IMC'
    ])
    
    for paciente in pacientes:
       
        fila_datos = [ 
           paciente.nombre, 
           paciente.primer_apellido, 
           paciente.segundo_apellido, 
           paciente.sexo,
            paciente.tipo.nombre, 
            paciente.nacionalidad.nombre, 
            paciente.comuna.nombre if paciente.comuna else "NO TIENE", 
            paciente.cesfam.nombre if paciente.cesfam else "NO TIENE", 
            paciente.direccion, 
            paciente.telefono, 
            paciente.tipo,
            paciente.identificacion, 
            paciente.fecha_nacimiento.strftime('%d-%m-%Y'),
            paciente.calcular_edad_paciente(), 
            "SI" if paciente.descapacitado else "NO",
            "SI" if paciente.pueblo_originario else "NO", 
            "SI" if paciente.privada_de_libertad else "NO",
            "SI" if paciente.transexual else "NO", 
            "SI" if paciente.plan_de_parto else "NO", 
            "SI" if paciente.visita_guiada else "NO", 
            paciente.peso, 
            paciente.altura, 
            paciente.calcular_imc()
            ]
    
        writer.writerow(fila_datos)

    return response


def parto_csv(request):

    response = HttpResponse(
        content_type="text/csv; charset=utf-8",
        headers={"Content-Disposition": 'attachment; filename="reporte_partos.csv"'},
    )

    response.write(codecs.BOM_UTF8) 
    
    partos = Parto.objects.select_related('via_nacimiento', 'tipo_de_ingreso', 'gestacion__paciente').order_by('-created_at')

    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    if start_date:
        partos = partos.filter(created_at__gte=start_date)
    
    if end_date:
        partos = partos.filter(created_at__lte=end_date)
    
    writer = csv.writer(response) 

    print(start_date)
    print(end_date)
    writer.writerow([
        "Nombre", "Tipo Documento", "Numero Documento", "Edad Madre", "Tipo de Ingreso", "Via Nacimiento", "Hora Inicio", 
        'Nº Tactos Vaginales', "Rotura de Membrana", "Posicion", "Tipo de Regimen",
        "Tipo de Inicio", "Tiempo Membrana Rota", "Tiempo Dilatacion",
        "Tiempo Expulsivo", "Entrega de Placenta", "Monitor", "Tipo de Acompañante",
        "Libertad de Movimiento", "Semanas de Gestacion", "Uso sala Saip", "Fecha Ingreso del Registro"
    ])
    
    for parto in partos:
        hora_inicio_str = parto.hora_inicio.strftime('%d-%m-%Y %H:%M') if parto.hora_inicio else ""
        
        fila_datos = [
            parto.gestacion.paciente.obtener_nombre_completo(), 
            parto.gestacion.paciente.documento,
            parto.gestacion.paciente.identificacion, 
            parto.edad_madre, 
            parto.tipo_de_ingreso.nombre, 
            parto.via_nacimiento.tipo, 
            hora_inicio_str,
            parto.n_tactos_vaginales if parto.n_tactos_vaginales is not None else "",
            parto.rotura_membrana, 
            parto.posicion, 
            parto.tipo_regimen, 
            parto.inicio_parto, 
            parto.tiempo_membrana_rota if parto.tiempo_membrana_rota is not None else "",
            parto.tiempo_dilatacion if parto.tiempo_dilatacion is not None else "",
            parto.tiempo_expulsivo if parto.tiempo_expulsivo is not None else "",
            "SI" if parto.entrega_placenta else "NO",
            "SI" if parto.monitor else "NO", 
            parto.tipo_acompaniante,
            "SI" if parto.libertad_movimiento else "NO", 
            parto.semanas_gestacion, 
            "SI" if parto.uso_sala_saip else "NO",
            parto.created_at.strftime('%d-%m-%Y %H:%M')
        ]
        
        writer.writerow(fila_datos)

    return response