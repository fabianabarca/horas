# Horas de TCU
Sistema de registro de horas de trabajo de estudiantes en el TCU

## Ejecutar Proyecto

`Actualizar base de datos`
- py manage.py makemigrations
- py manage.py migrate

`Levantar servidor`
- py manage.py runserver
- Ir a pagina principal servidor http://127.0.0.1:8000/cuentas/login/ o http://127.0.0.1:8000/ si logueado
## Esbozo de modelos de la aplicación de registro

`class Estudiante`

- Carné
- Correo
- Nombre
- Apellido
- Contraseña

`class Categoría`

- Nombre (por ejemplo: "desarrollo web", "prototipos", "talleres", "tutorías")

`class Proyecto`

- ID
- Nombre
- Descripción
- `profesor.id` (foreign key) (pueden ser varios)
- `categoria.id` (foreign key) (one to many)
- Ubicación
- Notas

`class Actividad`

- `estudiante.carné` (foreign key)
- `proyecto.id` (foreign key)
- Descripción
- Fecha
- Horas

`class Profesor`

- ID
- Correo
- Nombre
- Apellido
- Contraseña

`class Solicitud`

- `estudiante.carné` (foreign key)
- Tipo (finalización o prórroga o corrección de actividad)
- Motivo
- Fecha y hora

## Acciones por realizar

### Estudiantes

- Registrar horas
    - Colocar un botón grande que diga "+ Registrar actividad"
- Revisar horas realizadas
- Solicitudes de finalización/prórroga
- Mensaje a profesor(a)

### Profesores

- Revisión y aprobación/rechazo de actividades
- Consulta de horas totales por estudiantes
- Consulta de horas totales por proyecto
- Consulta de horas totales por etiqueta
- Creación de proyectos y actividades

### Siguientes pasos (menor prioridad)

- Generación de documentos (oficios de finalización o prórroga, etc.)
