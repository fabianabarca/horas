# Horas de TCU

Sistema de registro de horas de trabajo de estudiantes en el TCU.

## Componentes y vistas del sistema

Nota: los "proyectos" están compuestos de "tareas".

### Modo estudiantes

**Menú principal**
- **Registro de actividades**: enviar para revisión una actividad, indicando el día, las horas y una descripción.
![Registro de actividades](DesignImages/Estudiantes/RegistroDeActividades.PNG)
- **Gestiones administrativas**: hacer solicitudes de finalización, prórroga y corrección, explicando el motivo y adjuntando documentos si fuera necesario.
![GestionesAdministrativas](DesignImages/Estudiantes/GestionesAdministrativas.PNG)
- **Tareas**:
![Tareas](DesignImages/Estudiantes/Tareas.PNG)
### Modo profesores

**Menú principal**
- **Registro de actividades**: lista de todas las actividades registradas.
![Registro de actividades](DesignImages/Profesores/RegistroDeActividades.PNG)
- **Gestiones administrativas**: lista de solicitudes de gestiones administrativas.
![GestionesAdministrativas](DesignImages/Profesores/GestionesAdministrativas.PNG)
- **Tareas**: ver lista de tareas o crear una nueva con nombre, estudiante(s) asignado(s), proyecto asociado y descripción.
![Tareas](DesignImages/Profesores/Tareas.PNG)
- **Proyectos**: ver lista de proyectos o crear uno nuevo con nombre, descripción, profesor asignado, categoría y ubicación.
![Proyectos](DesignImages/Profesores/Proyectos.PNG)
- **Estudiantes**: lista de estudiantes activos.
![Estudiantes](DesignImages/Profesores/Estudiantes.PNG)

## Para ejecutar el proyecto localmente

**Crear base de datos**
- Eliminar las carpetas _migrations_ en cada folder
- Eliminar _db.sqlite3_
- Ejecutar `python manage.py makemigrations`
- Ejecutar `python manage.py migrate --run-syncdb`

**Instalar dependencias**
- py -m pip install django-crispy-forms

**Levantar servidor**
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
