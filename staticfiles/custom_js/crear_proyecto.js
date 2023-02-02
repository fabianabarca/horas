const descripcionObjetivos = []
let tmp_json 
let objetivos

function initializeObjectives(){
  //Puebla arreglo de descripciones con objetivos existentes.
  //A cada entrada le asigna el botón de borrado.
  for(let i = 0; i < objetivos.length; i++){
    descripcionObjetivos.push(objetivos[i].innerHTML)
    appendDeleteButton(i, objetivos[i])
  }

  //Valor default, indica si objetivos fueron modificados
  tmp_json.value = "!#!"
}

function saveObjective(){
  
  //Recupera div que contiene descripcion del objetivo
  const objForm = document.querySelector("#incluirObjetivo")

  //Del div que contiene form del objetivo, recupera campo de descripcion
  //del objetivo
  const descripcion = objForm.querySelector("#descripcionObjetivo")
  
  //No incluir objetivos vacíos
  if(descripcion.value != ""){
      //Recupera elemento <ul> que contendrá lista de objetivos definida por usuario
      const listaDeObjetivos = document.querySelector("#listaDeObjetivos")
      
      //Guarda descripcion del objetivo en arreglo temporal
      descripcionObjetivos.push(descripcion.value);
      
      //Crea elemento que dará feedback al usuario cuando este cree un objetivo
      //y puebla su contenido
      const nuevoObjetivo = document.createElement("li")
      nuevoObjetivo.id = descripcionObjetivos.length -1;
      nuevoObjetivo.innerHTML = descripcion.value
      
      appendDeleteButton(descripcionObjetivos.length -1, nuevoObjetivo)
      
      //Añade elemento recién creado a lista de objetivos
      listaDeObjetivos.appendChild(nuevoObjetivo)
      
      //Guarda string JSON de lista actual de objetivos en campo 
      //escondido de form de proyectos.
      tmp_json.value = JSON.stringify(descripcionObjetivos)
      
      descripcion.value = ""
    }
  }

  function appendDeleteButton(id, objectiveElement){
    //Crea botón e icono para eliminar objetivo
    const deleteButton = document.createElement("a")
    const trashIcon = document.createElement("i")
    //Asigna clases para que los elementos reciban estilos
    trashIcon.classList.add("icon")
    trashIcon.classList.add("cil-trash")
    deleteButton.classList.add("text-danger")
    //El elemento <a> adopta al icono para mejor UI
    deleteButton.appendChild(trashIcon)
    //Por último, el elemento <li> que contiene el objetivo
    //adopta a <a>
    objectiveElement.appendChild(deleteButton)
    
    deleteButton.addEventListener("click",()=>{
      //Elimina objetivo del arreglo y deja espacio vacío
      delete descripcionObjetivos[id]
      //Elimina el elemento del DOM
      objectiveElement.remove()

      //Guarda el arreglo actual
      tmp_json.value = JSON.stringify(descripcionObjetivos)
    
      console.log(`Objetivos: ${descripcionObjetivos}`)
    })

  }

  window.addEventListener('load',()=>{ 
    //Recupera field escondido del form que permitirá llevar string de objetivos
    //al servidor
    tmp_json = document.querySelector("#id_temp_obj_json")
    objetivos = document.getElementsByClassName("objetivo")
    initializeObjectives()
  })