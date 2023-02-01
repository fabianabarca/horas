// <!-- Confirmación de creación de registro -->

function confirmarRegistro() {
    var creacion = confirm('¿Está seguro/a de que desea crear el registro?');
    if (creacion) {
      const collection = document.getElementsByClassName("alert alert-success");

      collection[0].setAttribute("style", "display:block");
    }

    return creacion
}

$(document).ready(()=>{ $("#confirm").click(confirmarRegistro) })