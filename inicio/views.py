import json
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django import forms
from django.http.response import HttpResponseRedirect
import time
from cuentas.models import *
from actividades.models import Actividad
from cuentas.models import Estudiante
from proyectos.models import Proyecto
import datetime

def color_list_f(lista_cantidad_miembros):
    color_list = []
    alpha_initial = 1
    opasity_decrease_range = 0.2
    r = str(159)
    g = str(90)
    b = str(253)
    alpha = alpha_initial
    count = 0
    for i in lista_cantidad_miembros:
        alpha = alpha - (count)
        color = 'rgba(' + r + ',' + g + ',' + b + ',' + str(alpha) + ')'
        color_list.append(color)
        count = count + opasity_decrease_range
    return color_list

@login_required(login_url='/cuentas/ingreso/')
def index(request, id=9999):
    # En caso de que NO se redirige de página Estudiantes, uso el numero 9999 como default al llegar a
    # página Inicio desde login o desde menu de navegación
    if id == 9999:
        id = request.user.id

    # AQUÍ TODO LO QUE HAY QUE PONER EN EL PANEL DE PROFESOR
    if request.user.is_staff:
        estudiantes_list = Estudiante.objects.all()
        numero_estudiantes = estudiantes_list.filter(user__is_staff=False).count
        proyectos_list = Proyecto.objects.all()
        numero_proyectos = proyectos_list.count

        # Datos para horizontal bar chart con relación proyectos y actividades
        labels = []
        data = []
        dict_cantidad_actividades_horas = {}
        query_set_proyectos = Proyecto.objects.filter(enPapelera=False)

        for proyecto in query_set_proyectos:
            total_actividades_horas_por_proyecto = 0
            query_set_objetivos = proyecto.objetivo_set.filter(enPapelera=False)
            for objetivo in query_set_objetivos:
                query_set_tareas = objetivo.tarea_set.filter(enPapelera=False)
                # Cambio Metas a Tareas
                for tarea in query_set_tareas:
                    query_set_actividades = tarea.actividad_set.filter(
                        enPapelera=False)
                    for actividad in query_set_actividades:
                        total_actividades_horas_por_proyecto = total_actividades_horas_por_proyecto + actividad.horas
            dict_cantidad_actividades_horas[proyecto.nombre] = total_actividades_horas_por_proyecto

        sorted_dict_cantidad_actividades = sorted(
            dict_cantidad_actividades_horas.items(), key=lambda x: x[1], reverse=True)

        for element in sorted_dict_cantidad_actividades:
            labels.append(element[0])
            data.append(element[1])

        # Listas con los colores para los graficos desplegados
        color_list = color_list_f(dict_cantidad_actividades_horas)

        # A partir de aquí datos para grafico de barras ranking de estudiantes por actividades
        labels_ranking_estudiante = []
        data_ranking_estudiante = []
        ranking_indice_avance = []
        map_estudiante_cantidad_actividades = {}
        rankingEstudiantesList = Estudiante.objects.filter(user__is_staff=False)

        for estudiante in rankingEstudiantesList:
            horasActividades = Actividad.objects.filter(
                estudiante=estudiante, enPapelera=False)
            horas_estudiante = 0
            for actividad in horasActividades:
                horas_estudiante = horas_estudiante + actividad.horas
            map_estudiante_cantidad_actividades[estudiante] = horas_estudiante

        sorted_map_estudiante_cantidad_actividades = sorted(
            map_estudiante_cantidad_actividades.items(), key=lambda x: x[1], reverse=True)

        for element in sorted_map_estudiante_cantidad_actividades:
            labels_ranking_estudiante.append(element[0].user.username)
            data_ranking_estudiante.append(element[1])
            if(element[0].fecha_inicio != None):
                ranking_indice_avance.append(((100 / 300) * element[1]) / 
                ((100 / 365) * (datetime.date.today()-element[0].fecha_inicio).days))

        color_list_ranking_estudiante = color_list_f(map_estudiante_cantidad_actividades)

        inicio = 'panel.html'
        context = {
            "numero_estudiantes": numero_estudiantes,
            "numero_proyectos": numero_proyectos,
            "labels_ranking_estudiante": labels_ranking_estudiante,
            "data_ranking_estudiante": data_ranking_estudiante,
            "color_list_ranking_estudiante": color_list_ranking_estudiante,
            "ranking_indice_avance":ranking_indice_avance,
            "labels": labels,
            "data": data,
            "color_list": color_list,
        }
    
    # AQUÍ TODO LO QUE HAY QUE PONER EN EL PANEL DE ESTUDIANTE
    else:
        estudiante_actual = Estudiante.objects.get(user=request.user)

        # Desde aqui se procesa la barra de progreso de dias del TCU por estudiante
        current_datetime = datetime.date.today()
        inicio_TCU = estudiante_actual.fecha_inicio
        dias_desde_inicio_TCU = current_datetime - inicio_TCU
        dias_TCU = dias_desde_inicio_TCU.days
        total_dias_TCU = 365
        porcentaje_days_year = (100 / total_dias_TCU) * dias_TCU
        porcentaje_width_days_year = int(porcentaje_days_year)

        # Desde aqui se procesa la barra de progreso de horas por estudiante
        my_actividades_list = Actividad.objects.raw(
            'SELECT id, estudiante_id, horas, enPapelera FROM actividades_actividad where estudiante_id == ' + str(estudiante_actual.id)+" AND enPapelera==false")
        horas_totales_por_estudiante = 0

        for actividad in my_actividades_list:
            if actividad.estado == "A":
                horas_totales_por_estudiante += actividad.horas

        porcentaje = (100 / 300) * horas_totales_por_estudiante
        porcentaje_width = int(porcentaje)
        indice_avance = round(porcentaje / porcentaje_days_year, 2)
        indice_avance_width = int(50/1 * indice_avance)

        #Fechas, Horas Calendario
        actividades_calendario= Actividad.objects.raw('SELECT id, estudiante_id, horas, fecha, enPapelera FROM actividades_actividad where estudiante_id == '+ str(estudiante_actual.id)+" AND enPapelera==false AND estado == 'A'")
        horas_por_dia = [[0 for i in range(4)] for actividad in actividades_calendario]
        numero_actividades = 0
        for actividad in actividades_calendario:
            if actividad.estado == "A":
                horas_por_dia[numero_actividades][0]=actividad.fecha.year
                horas_por_dia[numero_actividades][1]=actividad.fecha.month
                horas_por_dia[numero_actividades][2]=actividad.fecha.day
                horas_por_dia[numero_actividades][3]=actividad.horas
                numero_actividades+=1

        inicio = 'resumen.html'
        context = {
            "progreso": horas_totales_por_estudiante,
            "width": porcentaje_width,
            "porcentaje_width_days_year": porcentaje_width_days_year,
            "indice_avance":indice_avance,
            "indice_avance_width":indice_avance_width,
            "horas_por_dia":json.dumps(horas_por_dia),
            "numero_actividades":numero_actividades,
        }

    return render(request, inicio, context)

def sitio(request):
    return render(request, "sitio.html")
