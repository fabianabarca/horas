# Aplicaciones de Django

1. actividades
1. areas
1. cuentas
1. dashboard
1. estudiantes
1. horas
1. inicio
1. objetivos
1. papelera
1. proyectos
1. solicitudes
1. tareas

# Menú lateral

Revisión

## Profesores

- [ ] Nuevo registro
- [ ] Panel
- [ ] Actividades
- [ ] Tareas
- [ ] Proyectos
- [ ] Áreas
- [ ] Solicitudes
- [ ] Estudiantes

## Estudiantes

- [ ] Nuevo registro
- [x] Resumen
- [x] Actividades
- [ ] Tareas
- [x] Proyectos
- [x] Áreas
- [x] Solicitudes

# Mapa del sitio

- `tropicalizacion.eie.ucr.ac.cr`: página de inicio del TCU con información general
  - `/proyectos`: una lista de los proyectos del TCU
    - `/[proyecto]`: información del proyecto (objetivos, metas, tareas, fotos...)
  - `/contacto`
  - `/sistema`: sistema de registro de horas
    - `/estudiante`: información para estudiantes registrados
    - `/profesor`: panel de administración de profesores

## Bases HTML

- `sitio.html`: plantilla del sitio de información
- `sistema.html`: plantilla del panel de administración
