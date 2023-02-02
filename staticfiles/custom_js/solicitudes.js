$("document").ready(()=>{
    $(".fila_tabla").click(function () {
        $('#myModal').modal('show')
        var row = $(this).closest("tr");
        var motivo = row.find(".label.Motivo").html()
        var fecha = row.find(".label.Fecha").html()
        var carne = row.find(".label.Carne").html()
        var nombre = row.find(".label.Nombre").html()
        var correo = row.find(".label.Correo").html()
        //var archivo = row.find(".label.Archivo").html()
        var estado = row.find(".label.Estado").html()

        $('#d_motivo').text(motivo)
        $('#d_fecha').text(fecha)
        $('#d_carne').text(carne)
        $('#d_nombre').text(nombre)
        $('#d_correo').text(correo)
        //$('#d_archivo').text(motivo)
        $('#d_estado').text(estado)
    });

    //OCULTAR LAS COLUMNAS CORRESPONDIENTES

    $('td:nth-child(4),th:nth-child(4)').hide();
    $('td:nth-child(6),th:nth-child(6)').hide();
    //$('td:nth-child(7),th:nth-child(7)').hide();
})