import json
from tkinter import W
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
from datetime import timedelta

# Recibe: Diccionario o lista con elementos y sus cantidades
# Modifica: ---
# Devuelve: Lista con los colores para los gráficos desplegados
def color_list_f(lista_cantidad_miembros):
    # Datos de la lista
    color_list = []
    alpha_initial = 1
    opasity_decrease_range = 0.2
    r = str(159)
    g = str(90)
    b = str(253)
    alpha = alpha_initial
    count = 0

    # Por cada miembro del diccionario agrega los colores a la nueva lista:
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

    # Información para panel de profesores
    # ------------------------------------
    if request.user.is_staff:
        # Datos de números de estudiantes y proyectos #
        estudiantes_list = Estudiante.objects.all() # Lista de estudiantes a trabajar
        numero_estudiantes = estudiantes_list.filter(user__is_staff=False).count # Cantidad de estudiantes
        proyectos_list = Proyecto.objects.all() # Lista de proyectos a trabajar
        numero_proyectos = proyectos_list.count # Cantidad de proyectos

        # Datos para "horizontal bar chart" con relación proyectos y actividades #
        labels = [] # Etiquetas para el gráfico
        data = [] # Datos para el gráfico
        dict_cantidad_actividades_horas = {} # Diccionario de proyectos y sus horas
        query_set_proyectos = Proyecto.objects.filter(enPapelera=False) # Proyectos existentes

        # Llenar el diccionario de Proyectos y sus cantidades de horas
        for proyecto in query_set_proyectos:
            total_actividades_horas_por_proyecto = 0
            query_set_objetivos = proyecto.objetivo_set.filter(enPapelera=False)
            for objetivo in query_set_objetivos:
                query_set_tareas = objetivo.tarea_set.filter(enPapelera=False)
                for tarea in query_set_tareas:
                    query_set_actividades = tarea.actividad_set.filter(
                        enPapelera=False)
                    for actividad in query_set_actividades:
                        total_actividades_horas_por_proyecto = total_actividades_horas_por_proyecto + actividad.horas
            dict_cantidad_actividades_horas[proyecto.nombre] = total_actividades_horas_por_proyecto

        # Ordenar el diccionario de actividades por sus cantidades de horas
        sorted_dict_cantidad_actividades = sorted(
            dict_cantidad_actividades_horas.items(), key=lambda x: x[1], reverse=True)

        # Llenar las listas de etiquetas y datos para los gráficos
        for element in sorted_dict_cantidad_actividades:
            labels.append(element[0])
            data.append(element[1])

        # Listas con los colores para los gráficos desplegados
        color_list = color_list_f(dict_cantidad_actividades_horas)

        # A partir de aquí datos para grafico de barras: ranking por índice de avance #
        labels_ranking_estudiante = [] # Etiquetas del gráfico de ranking
        data_ranking_estudiante = [] # Datos del gráfico de ranking
        map_estudiante_cantidad_actividades = {} # Mapa de estudiantes con sus cantidades de horas
        ranking_estudiantes_list = Estudiante.objects.filter(user__is_staff=False) #  Lista de estudiantes para el ranking
        # Variables para el cálculo de índice de avance para el ranking
        ranking_indice_avance = [] # Datos del índice de avance para el ranking
        porcentaje_horas = 0 # Porcentaje de avance de horas, valor mínimo 0.01
        porcentaje_tiempo = 0 # Porcentaje de avance del tiempo disponible, valor mínimo 0.01
        indice_avance_total = 0 # Índice de avance con todos los decimales
        indice_avance = 0 # Índice de avance redondeado a dos decimales
        fecha_hoy = datetime.date.today() # Fecha del día actual de tipo fecha
        dias_desde_inicio_TCU = 0 # Días transcurridos desde el inicio del TCU para el estudiante

        # Llenar el mapa de estudiantes con sus horas respectivas
        for estudiante in ranking_estudiantes_list:
            horas_actividades = Actividad.objects.filter(
                estudiante=estudiante, enPapelera=False)

            horas_estudiante = 0
            for actividad in horas_actividades:
                horas_estudiante = horas_estudiante + actividad.horas
            map_estudiante_cantidad_actividades[estudiante] = horas_estudiante

        # Ordenar el mapa de estudiantes por sus cantidades de horas
        sorted_map_estudiante_cantidad_actividades = sorted(
            map_estudiante_cantidad_actividades.items(), key=lambda x: x[1], reverse=True)

        # Llenar las listas de etiquetas y datos para los gráficos de rankings
        for element in sorted_map_estudiante_cantidad_actividades:
            labels_ranking_estudiante.append(element[0].user.username)
            data_ranking_estudiante.append(element[1])
            if(element[0].fecha_inicio != None): # Si la fecha de inicio no es nula:
                dias_desde_inicio_TCU = (fecha_hoy - element[0].fecha_inicio).days
                porcentaje_horas = (100 / 300) * element[1]
                porcentaje_tiempo = (100 / 365) * dias_desde_inicio_TCU
                if(porcentaje_horas == 0): # Cambia el porcentaje de horas si es 0 al mínimo para mantener el índice correcto
                    porcentaje_horas = 0.01
                if(porcentaje_tiempo == 0): # Cambia el porcentaje de tiempo si es 0 al mínimo para evitar errores de cálculo
                    porcentaje_tiempo = 0.01
                indice_avance_total = porcentaje_horas / porcentaje_tiempo # Calcula el índice de avance total
                indice_avance = round(indice_avance_total, 2) # Limita a 2 decimales el índice de avance
                ranking_indice_avance.append(indice_avance) # Agrega al ranking el índice de avance

        # Calcular la lista de colores para los gráficos desplegados
        color_list_ranking_estudiante = color_list_f(map_estudiante_cantidad_actividades)

        # Inicio y contexto si el usuario es profesor #
        inicio = 'panel.html'
        context = {
            "numero_estudiantes": numero_estudiantes, # Cantidad de estudiantes
            "numero_proyectos": numero_proyectos, # Cantidad de proyectos
            "labels_ranking_estudiante": labels_ranking_estudiante, # Etiquetas del gráfico de ranking
            "data_ranking_estudiante": data_ranking_estudiante, # Datos del gráfico de ranking
            "color_list_ranking_estudiante": color_list_ranking_estudiante, # Lista de colores para los gráficos desplegados
            "ranking_indice_avance": ranking_indice_avance, # Datos del índice de avance para el ranking
            "labels": labels, # Etiquetas para el gráfico
            "data": data, # Datos para el gráfico
            "color_list": color_list, # Listas con los colores para los gráficos desplegados
        }
    
    # Información para resumen de estudiantes
    # ---------------------------------------
    else:
        estudiante_actual = Estudiante.objects.get(user=request.user) # Estudiante actual a trabajar

        # Desde aqui se procesa la barra de progreso de dias del TCU por estudiante #
        fecha_hoy = datetime.date.today() # Fecha del día actual de tipo fecha
        inicio_TCU = estudiante_actual.fecha_inicio # Fecha de inicio del TCU del estudiante actual
        dias_desde_inicio_TCU = (fecha_hoy - inicio_TCU).days # Días transcurridos desde el inicio del TCU para el estudiante
        porcentaje_tiempo = (100 / 365) * dias_desde_inicio_TCU # Porcentaje de avance del tiempo disponible, valor mínimo 0.01
        porcentaje_tiempo_width = int(porcentaje_tiempo) # Entero del porcentaje de avance del tiempo disponible para el widget

        # Desde aqui se procesa la barra de progreso de horas por estudiante #
        my_actividades_list = Actividad.objects.raw( # Lista de actividades del estudiante
            'SELECT id, estudiante_id, horas, enPapelera FROM actividades_actividad where estudiante_id == ' + str(estudiante_actual.id)+" AND enPapelera==false")
        horas_totales_por_estudiante = 0 # Horas totales del estudiante actual

        # Calcula la sumatoria de horas entre todas las actividades del estudiante
        for actividad in my_actividades_list:
            if actividad.estado == "A":
                horas_totales_por_estudiante += actividad.horas

        # Variables para los datos de las barras de widgets horas e índice
        porcentaje_horas = (100 / 300) * horas_totales_por_estudiante # Porcentaje de avance de horas, valor mínimo 0.01
        porcentaje_horas_width = int(porcentaje_horas) # Entero del porcentaje de avance de horas
        if(porcentaje_horas == 0): # Cambia el porcentaje de horas si es 0 al mínimo para mantener el índice correcto
            porcentaje_horas = 0.01
        if(porcentaje_tiempo == 0): # Cambia el porcentaje de tiempo si es 0 al mínimo para evitar errores de cálculo
            porcentaje_tiempo = 0.01
        indice_avance_total = porcentaje_horas / porcentaje_tiempo # Índice de avance con todos los decimales
        indice_avance = round(indice_avance_total, 2) # Índice de avance redondeado a dos decimales
        indice_avance_width = int(100 * indice_avance) # Porcentaje de la barra para mostrar el índice de avance

        # Calendario de Google Charts tipo heatmap de Github #
        actividades_calendario = Actividad.objects.raw( # Selecciona las actividades del estudiante
            'SELECT id, estudiante_id, horas, fecha, enPapelera FROM actividades_actividad where estudiante_id == '
            + str(estudiante_actual.id)+" AND enPapelera==false AND estado == 'A'")
        horas_por_dia = [[0 for i in range(4)] for actividad in actividades_calendario] # Lista para los datos del calendario
        numero_actividades = 0 # Número de actividades del estudiante
        
        # Calcula los datos utilizados en el calendario de Google Charts tipo heatmap de Github
        for actividad in actividades_calendario: # Por cada actividad
            if actividad.estado == "A": # Si el estado es Activo
                horas_por_dia[numero_actividades][0]=actividad.fecha.year # Año de la actividad
                horas_por_dia[numero_actividades][1]=actividad.fecha.month # Mes de la actividad
                horas_por_dia[numero_actividades][2]=actividad.fecha.day # Día de la actividad
                horas_por_dia[numero_actividades][3]=actividad.horas # Horas de la actividad
                numero_actividades+=1 # Cantidad de actividades


        #[Calcular la cantidad de horas aprobadas en los últimos 7 días de cada estudiante]

        #Calcular el ultimo dia de los 7 de la semana, (dia actual - 7)
        fecha_primer_dia = fecha_hoy - timedelta(days=6)
        primer_dia = fecha_primer_dia.day

        #Arreglo para almacenar las actividades registradas en los últimos 7 días
        actividades_semana = []
        act_indx = 0
        for actividad in horas_por_dia:
            if(horas_por_dia[act_indx][0] == fecha_hoy.year and (horas_por_dia[act_indx][1] == fecha_hoy.month or horas_por_dia[act_indx][1] == fecha_hoy.month-1) ):
                if(horas_por_dia[act_indx][2] >= primer_dia and horas_por_dia[act_indx][2] <= fecha_hoy.day):
                    actividades_semana.append(horas_por_dia[act_indx])
            act_indx+=1

        #Ordenar actividades_semana por la fecha del día
        actividades_semana.sort()

        #Almacena la cantidad de horas por cada uno de los 7 ultimos dias
        horas_semana = [0] * 7
        #indice para el arreglo horas_semana
        horas_indx = 0
        #indice para actividades_semana
        act_fila = 0
        
        #Variable para controlar cual es el dia actual dentro del ciclo
        pr_day = primer_dia

        for activity in actividades_semana:
            if(pr_day != actividades_semana[act_fila][2]):
                horas_indx += (actividades_semana[act_fila][2] - pr_day)
            
            horas_semana[horas_indx]+= actividades_semana[act_fila][3]
            pr_day = actividades_semana[act_fila][2]
            act_fila+=1


        #Almacena el nombre de los dias para enviarlo al grafico
        dias_labels = []
        #Arreglo con los nombres de los dias de la semana
        dias_semana = ['Lunes', 'Martes', 'Miercoles', 'Jueves', 'Viernes', 'Sabado', 'Domingo']
        #Se obtiene el numero del utimo dia en la semana
        ultimo_dia = fecha_primer_dia.weekday()

        dias_indx = ultimo_dia

        while (dias_indx <= 6):
            dias_labels.append(dias_semana[dias_indx])
            dias_indx += 1
            if(dias_indx == 7):
                dias_indx = 0
            if(dias_indx == ultimo_dia):
                break


        # Inicio y contexto si el usuario es estudiante #
        inicio = 'resumen.html'
        context = {
            "estudiante": estudiante_actual,
            "horas_totales_por_estudiante": horas_totales_por_estudiante, # Horas totales del estudiante actual
            "dias_desde_inicio_TCU": dias_desde_inicio_TCU,
            "porcentaje_horas_width": porcentaje_horas_width, # Entero del porcentaje de avance de horas
            "porcentaje_tiempo_width": porcentaje_tiempo_width, # Entero del porcentaje de avance del tiempo disponible para el widget
            "indice_avance": indice_avance, # Índice de avance redondeado a dos decimales
            "indice_avance_width": indice_avance_width, # Porcentaje de la barra para mostrar el índice de avance
            "horas_por_dia": json.dumps(horas_por_dia), # Lista para los datos del calendario, convertida con json
            "numero_actividades": numero_actividades, # Número de actividades del estudiante
            "horas_semanales": json.dumps(horas_semana),
            "dias_semana": json.dumps(dias_labels)
        }

    # Inicio y contexto según el usuario sea estudiante o profesor
    return render(request, inicio, context)

def sitio(request):
    return render(request, "sitio.html")