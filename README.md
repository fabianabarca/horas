# Horas de TCU
Sistema de registro de horas de trabajo de estudiantes en el TCU

## Esbozo de modelos de la aplicación de registro

`class Estudiante`

- Carné
- Correo
- Nombre
- Apellido
- Contraseña

`class Proyecto`

- ID
- Nombre
- profesor.id (foreign key) (pueden ser varios)
- Etiquetas o categorías (por ejemplo: "desarrollo web", "prototipos", "talleres", "tutorías")
- (Ubicación, socios, etc.)

``class Actividad``

- estudiante.carné (foreign key)
- proyecto.id (foreign key)
- Descripción
- Fecha
- Horas

`class Profesor`

- ID
- Correo
- Nombre
- Apellido
- Contraseña

## Acciones por realizar

### Estudiantes

- Registrar horas
- Revisar horas realizadas
- Solicitudes de finalización/prórroga
- Solicitudes de remoción/modificación horas

### Profesores

- Revisión y aprobación/rechazo de actividades
- Consulta de horas totales por estudiantes
- Consulta de horas totales por proyecto
- Consulta de horas totales por etiqueta
- Creación de proyectos

### Siguientes pasos (menor prioridad)

- Sistema de mensajería
- Generación de documentos (oficios de finalización o prórroga, etc.)
