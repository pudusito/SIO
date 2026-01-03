from django.shortcuts import render

def inicio_reportes(request):
    return render(request, 'reportes/inicio_reportes.html')