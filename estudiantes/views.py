from django import forms
from django.http.response import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from cuentas.models import *
from horas.forms import EstudiantesForm
from actividades.models import Actividad
from proyectos.models import Proyecto
import datetime

from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url='/cuentas/login/')
def estudiantes_request(request):

    staffBotonVistaEstudiante= False

    if request.method == "POST":
        list_of_inputs=request.POST.getlist('inputs')
        if request.POST.get('studentButton'):
                studentButtonItemValue=request.POST.getlist('studentButton')
                estudianteAVer = Estudiante.objects.filter(id = studentButtonItemValue[0])
                staffBotonVistaEstudiante = True
                #response = HttpResponseRedirect("/")
                #response.headers["estudiante"] = estudianteAVer[0].id
                #return response
                estudiante_actual = estudianteAVer[0]

     
                estudiantes_list = Estudiante.objects.all()

                numeroEstudiantes=estudiantes_list.filter(user__is_staff=False).count

                proyectos_list = Proyecto.objects.all()
                numeroProyectos=proyectos_list.count
                

                #Desde aqui se procesa la barra de progreso de horas por estudiante
                my_actividades_list= Actividad.objects.raw('SELECT id, estudiante_id, horas, enPapelera FROM actividades_actividad where estudiante_id == '+ str(estudiante_actual.id)+" AND enPapelera==false")
                horasTotalesPorEstudiante=0      
                for actividad in my_actividades_list:
                    if actividad.estado == "A":
                        horasTotalesPorEstudiante+= actividad.horas

                #horasTotalesPorEstudiante=30  #para pruebas
                porcentaje= (100 / 300) * horasTotalesPorEstudiante
                porcentajeWidth = int(porcentaje)


                #Desde aqui se procesa la barra de progreso de dias del TCU por estudiante
                current_datetime = datetime.date.today()
                inicioTCU = estudiante_actual.fechaInicioTCU
                finalTCU = estudiante_actual.fechaFinTCU

                diasRestantesDelTCU =  finalTCU - current_datetime

                diasDesdeInicioTCU = current_datetime - inicioTCU
                diasTCU = diasDesdeInicioTCU.days

                totalDiasTCU = 365

                porcentajeDaysYear= (100 / totalDiasTCU) * diasTCU
                porcentajeWidthDaysYear = int(porcentajeDaysYear)


                factorDeAvance =  porcentaje / porcentajeDaysYear
                redondeadoFactorDeAvance = int(factorDeAvance)

                #Desde aqui se procesan los registros que esta realizando actualmente
                actividades_list = Actividad.objects.filter(estudiante = estudiante_actual)
                proyectos_list = Proyecto.objects.filter(objetivo__meta__tarea__actividad__estudiante = estudiante_actual)

                listaDirectorio = []

                for actividad in actividades_list:
                    listaHaciaActividad = []
                    listaHaciaActividad.append(actividad.descripcion)
                    tarea = actividad.tarea

                    listaHaciaActividad.append(tarea.nombre)
                    meta = tarea.meta            

                    listaHaciaActividad.append(meta.nombre)
                    objetivo = meta.objetivo

                    listaHaciaActividad.append(objetivo.nombre)
                    proyecto = objetivo.proyecto

                    listaHaciaActividad.append(proyecto.nombre)
                    listaDirectorio.append(listaHaciaActividad)

                listaProyectos = {}
                listaObjetivos = {}
                listaMetas = {}
                listaTareas = {}
                listaActividades = {}



                for listaCamino in listaDirectorio:
                
                    #si no existe  en diccionario, se agrega con lista vacia
                    if not listaCamino[4] in listaProyectos:
                        listaProyectos[listaCamino[4]] = list[""]
                        #con el proyecto agregado ahora se agrega objetivo respectivo
                        #formato de elementos de diccionarios: {"nombreproyecto",sublistaObjetivos["",dic{nombreObjetivo,list[""}]}]}
                    
                    else:
                    #si  existe  en diccionario, se le agrega la subcategoria
                        listaObjetivos
                        if not listaCamino[3] in listaObjetivos:
                            listaObjetivos[listaCamino[3]] = list[""]

                        else:
                            listaMetas
                            if not listaCamino[2] in listaMetas:
                                listaMetas[listaCamino[2]] = list[""]

                            
                            else:
                                listaTareas
                                if not listaCamino[1] in listaTareas:
                                    listaTareas[listaCamino[1]] = list[""]

                                else:
                                    listaActividades
                                    if not listaCamino[0] in listaActividades:
                                        listaActividades[listaCamino[0]] = list[""]

                                    else:

                                        updateList=  listaProyectos[listaCamino[4]]
                                        updateList.append(listaCamino[3]) 
                                        #car.update({"brand": "White"})

                                        listaProyectos[listaCamino[4]] 


                #Creando formato de directorio para actividades de estudiante actual
                listaProyectos = {}
                listaObjetivos = {}
                listaMetas = {}
                listaTareas = {}
                listaActividades = []        
                querysetProyectos=Proyecto.objects.filter(objetivo__meta__tarea__actividad__estudiante = estudiante_actual)       
                for proyecto in querysetProyectos:
                    if (proyecto.enPapelera==False):
                        totalActividadesPorProyecto = 0
                        querysetObjetivos=proyecto.objetivo_set.all()
                        querysetObjetivos=querysetObjetivos.filter(meta__tarea__actividad__estudiante = estudiante_actual)  

                        listaProyectos[proyecto.nombre] = listaObjetivos
                        listaObjetivos = {}
                        for objetivo in querysetObjetivos:
                            if (objetivo.enPapelera==False):
                                querysetMetas=objetivo.meta_set.all()
                                querysetMetas=querysetMetas.filter(tarea__actividad__estudiante = estudiante_actual)  


                                listaMetas = {}
                                for meta in querysetMetas:
                                    if (meta.enPapelera==False):
                                        querysetTareas=meta.tarea_set.all()
                                        querysetTareas=querysetTareas.filter(actividad__estudiante = estudiante_actual)  


                                    
                                        listaTareas = {}
                                        for tarea in querysetTareas:
                                            if (tarea.enPapelera==False):
                                                #print("testing actividad descripcion " + actividad.descripcion)
                                                querysetActividades=tarea.actividad_set.all()
                                                querysetActividades=querysetActividades.filter(estudiante = estudiante_actual)  

                                                #if tarea.nombre in listaTareas:
                                                listaActividades = [] 
                                                for actividad in querysetActividades:
                                                        if (actividad.enPapelera==False):
                                                            #print("testing actividad descripcion" + actividad.descripcion)
                                                            listaActividades.append(actividad.descripcion)
                                                    
                                                listaTareas[tarea.nombre] = listaActividades

                                        listaMetas[meta.nombre] = listaTareas

                                listaObjetivos[objetivo.nombre] = listaMetas
                            
                        listaProyectos[proyecto.nombre] = listaObjetivos
            


                #Creando string de directorios de actividades
                #print("probando")
                directorioActividades = []
                stringHierarchy = []
                listaProyectosKeys = listaProyectos.keys()
                for proyecto in listaProyectosKeys:
                
                    #print("Proyecto: " + proyecto + "\n")   
                    directorioActividades0 = ""
                    directorioActividades0 = directorioActividades0 +"Proyecto:     " + proyecto + "\n"  
                    directorioActividades.append(directorioActividades0)
                    stringHierarchy.append("proyecto")
                    listaObjetivosKeys = listaProyectos[proyecto].keys()
                    listaObjetivos = listaProyectos[proyecto]

                    for objetivo in listaObjetivosKeys:
                        #print("     objetivo: " +objetivo + "\n")  
                        directorioActividades1 = ""
                        directorioActividades1 = directorioActividades1 +"-Objetivo:   " +objetivo + "\n"
                        directorioActividades.append(directorioActividades1)
                        stringHierarchy.append("objetivo")
                        listaMetasKeys = listaObjetivos[objetivo].keys()
                        listaMetas = listaObjetivos[objetivo]

                        for meta in listaMetasKeys:
                            #print("         meta: " +meta + "\n") 
                            directorioActividades2 = ""
                            directorioActividades2 = directorioActividades2 +"--        "+"Meta:     " +meta + "\n"
                            directorioActividades.append(directorioActividades2)
                            stringHierarchy.append("meta")
                            listaTareasKeys = listaMetas[meta].keys()
                            listaTareas = listaMetas[meta]

                            for tarea in listaTareasKeys:
                                #print("             tarea: " +tarea + "\n")  
                                directorioActividades3 = ""
                                directorioActividades3 = directorioActividades3 +"-----             Tarea:     " +tarea + "\n" 
                                directorioActividades.append(directorioActividades3)
                                stringHierarchy.append("tarea")
                                #listaActividadesKeys = listaTareasKeys[actividad].keys()
                                listaActividades = listaTareas[tarea]

                                for actividad in listaActividades:
                                    if Actividad.objects.filter(descripcion=actividad)[0].estudiante==estudiante_actual:
                                        #print("                 actividad: " +actividad + "\n")  
                                        directorioActividades4 = ""
                                        directorioActividades4 = directorioActividades4 +"------------                Actividad:   " +actividad + "\n" 
                                        stringHierarchy.append("actividad")
                                        directorioActividades.append(directorioActividades4)
                                    
                                    
                                                            
                #print("chequeo string")
                

                zipDirectorio= zip(stringHierarchy,directorioActividades)

                return render (request=request, template_name="../templates/indexEstudiante.html", context={"progreso":horasTotalesPorEstudiante,
                "porcentaje":porcentaje,"width":porcentajeWidth,"diasTCU":diasTCU,"inicioTCU":inicioTCU,"finalTCU":finalTCU,"totalDiasTCU":totalDiasTCU,
                "porcentajeDaysYear":porcentajeDaysYear,"porcentajeWidthDaysYear":porcentajeWidthDaysYear,"factorDeAvance":factorDeAvance,
                "numeroEstudiantes":numeroEstudiantes,"numeroProyectos":numeroProyectos,"estudiante_actual":estudiante_actual
                ,"proyectos_list":proyectos_list,"listaDirectorio":listaDirectorio,"actividades_list":actividades_list,
                "zipDirectorio":zipDirectorio,})


    estudiantes_list = Estudiante.objects.all().filter(user__is_staff=False)
    if request.user.is_staff:
        actividades_list = Actividad.objects.all()
    Actividad.objects.raw('SELECT id, horas FROM myapp_actividad ')
    horasEstudianteslist = []
    porcentajeEstudianteslist = []
    porcentajeWidthEstudianteslist = []

    horasTotalesPorEstudiante=0
    for estudiante in estudiantes_list:
       

        horasTotalesPorEstudiante=0
        for actividad in actividades_list:
            
            if actividad.estudiante.user.username == estudiante.user.username:
                if actividad.estado == "A":
                    horasTotalesPorEstudiante+= actividad.horas

        horasEstudianteslist.append(horasTotalesPorEstudiante)
        porcentaje= (100 / 300) * horasTotalesPorEstudiante
        porcentajeEstudianteslist.append(porcentaje)
        porcentajeWidthEstudianteslist.append(int(porcentaje))

    zipHoras= zip(estudiantes_list,horasEstudianteslist,porcentajeEstudianteslist,porcentajeWidthEstudianteslist)    
    
    return render (request=request, template_name="../templates/estudiantes.html", context={"zipHoras":zipHoras,"horaslist":horasEstudianteslist,
    "estudiantes":estudiantes_list,"actividades":actividades_list,
    "porcentajeList":porcentajeEstudianteslist,"porcentajeWidthList":porcentajeWidthEstudianteslist})

@login_required(login_url='/cuentas/login/')
def editar_estudiante(request, id):

    obj = get_object_or_404(Estudiante, id = id) 

    form = EstudiantesForm(request.POST or None, instance = obj)
    form.fields['user'].widget = forms.HiddenInput()
    form.fields['carrera'].widget = forms.HiddenInput()
    form.fields['fechaInicioTCU'].widget = forms.HiddenInput()
    form.fields['fechaFinTCU'].widget = forms.HiddenInput()

    if form.is_valid():
        form.save()
        return HttpResponseRedirect("/estudiantes")

 
    return render(request, "editar_estudiante.html", context={"estudiante_form":form})