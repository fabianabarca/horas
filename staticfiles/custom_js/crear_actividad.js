let initial_project_id 
let initial_obj_id 
let initial_tarea_id 

function clear_options(){
    $('#id_proyecto').empty();
    $('#id_objetivo').empty();
    $('#id_tarea').empty();
}

//<!--Para cargar los proyectos del area-->
function update_projects() {
    var url = $("#crear_actividad_form").attr("proyectos-url");
    var areaId = $("#id_area").val();
    $.ajax({
        url: url,
        data: {
        'area':areaId
        },
        success: function (data){
        $("#id_proyecto").html(data);
        //Cuando editamos una actividad, un proyecto ya fue elegido anteriormente.
        //Este if es para  setear nuevamente el valor original elegido en editar_actividad.
        if(initial_project_id != null){
            $("#id_proyecto").val(initial_project_id)
            //Vacía valor para que no ingrese más de dos veces.
            initial_project_id = null
        }
        }
    })
}

// <!--Para cargar los objetivos del proyecto-->
function update_objectives() {
    var url = $("#crear_actividad_form").attr("objetivos-url");
    var proyectoId = $("#id_proyecto").val();
    $.ajax({
        url: url,
        data: {
        'proyecto':proyectoId
        },
        success: function (data){
        $("#id_objetivo").html(data);
        if(initial_obj_id != null){
            $("#id_objetivo").val(initial_obj_id)
            initial_obj_id = null
        }
        }
    });

}

// <!--Para cargar las tareas-->
function update_tareas() {
    var url = $("#crear_actividad_form").attr("tareas-url");
    var objetivoId = $("#id_objetivo").val();
    $.ajax({
        url: url,
        data: {
        'objetivo':objetivoId
        },
        success: function (data){
        $("#id_tarea").html(data);
        if(initial_tarea_id != null){
            $("#id_tarea").val(initial_tarea_id)
            initial_tarea_id = null
        }
        }
    });
}



var formSubmitting = false;
var setFormSubmitting = function () { formSubmitting = true; };

window.onload = function () {
window.addEventListener("beforeunload", function (e) {
    if (formSubmitting) {
    return undefined;
    }

    var confirmationMessage = 'It looks like you have been editing something. '
    + 'If you leave before saving, your changes will be lost.';

    (e || window.event).returnValue = confirmationMessage; //Gecko + IE
    return confirmationMessage; //Gecko + Webkit, Safari, Chrome etc.
});
};


//Cuando el DOM de la página carga...
$(document).ready(()=>{
    
    //Recupera valores de la actividad elegida(si el usuario ingresa a editar_actividad)
    initial_project_id = $("#id_proyecto").val();
    initial_obj_id =  $("#id_objetivo").val()
    initial_tarea_id =  $("#id_tarea").val()
   
    //Ejecuta este método para cargar lista de proyectos basados
    //en área seteada anteriormente cuando carga la página. 
    //Usada para editar_actividad
    update_projects()
    update_objectives()
    update_tareas()  

    $("#id_proyecto").click(update_objectives);
    $("#id_objetivo").click(update_tareas);
  //  $("#confirm").click(confirmarRegistro);
    $("#id_area").change(clear_options);
    $("#id_area").change(update_projects);
})