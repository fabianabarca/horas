//Este script desactiva el required de los campos de contraseña y usuario
//cuando el campo de carnet está poblado. Reactiva required si el campo está vacío.
let carnetField 
let userField 
let passwordField 

function validarCarnet(){
    if(carnetField.value != ""){
        userField.required = false;
        passwordField.required = false;
    }else{
        userField.required = true;
        passwordField.required = true;
    }
}

window.addEventListener("load",()=>{
    carnetField = document.querySelector("#id_carnet")
    userField = document.querySelector("#id_username")
    passwordField = document.querySelector("#id_password")
})