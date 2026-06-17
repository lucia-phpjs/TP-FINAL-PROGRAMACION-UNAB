# TP-FINAL-PROGRAMACION-UNAB

# Sistema de Gestión de Entrevistas Laborales

## Descripción

Proyecto academico desarrollada en Python para la gestión de procesos de selección de personal.

Permite registrar candidatos, crear búsquedas laborales, realizar evaluaciones y gestionar turnos de entrevistas mediante una interfaz web desarrollada con Flask.

El proyecto fue desarrollado aplicando Programación Orientada a Objetos (POO), separando la lógica de negocio, los modelos y la interfaz de usuario.

El sistema permite:

* Registrar candidatos: 
Se dan de alta postulantes validando que no existan correos duplicados. 
Al ingresar al sistema se les da de estado automático "Pendiente".
* Crear búsquedas laborales:
Se crean puestos con requisitos mínimos de experiencia y habilidades requeridas.
* Evaluar candidatos: 
Se vincula un candidato con una búsqueda laboral y un evaluador.
Al calificarlo (Con puntuación numérica) el estado del candidato
cambia a Aprobado o Rechazado.
* Agendar entrevistas:
Para los candidatos aprobados, se reserva un turno con fecha,hora, entrevistador y
sala de reuniones, validando previamente que la sala nos e encuentre ocupada
en esa misma franja horaria.
* Generar datos de demostración automáticamente: Para fácil testeo.




### Versión Web

Aplicación web desarrollada con Flask a partir de la lógica de negocio existente.
Recordatorio: es necesario tener instalado Flask - pip install flask -

Ejecución:
```bash
python app.py
```

Acceso:

http://127.0.0.1:5000


## Tecnologías utilizadas

* Python 3
* Flask (Arquitectura y renderizado de plantillas)
* HTML5
* CSS3
* JavaScript
* Programación Orientada a Objetos

## Estructura

```text
│
├── main.py                     # Punto de entrada principal y rutas del servidor Flask
├── app.py                      # Script secundario de inicialización de la app
│
├── modelos/                     # Capa de entidades de negocio (Clases base)
│   ├── agenda.py               # Gestión de turnos y salas de entrevista
│   ├── empleos.py              # Definición de búsquedas laborales y evaluaciones
│   └── usuarios.py             # Entidades candidato, reclutador y administradores
│
├── servicios/                  # Capa de lógica y orquestación (Controladores)
│   ├── gestores.py             # Servicios específicos de negocio (Candidato, Evaluacion, Calendario)
│   └── sistema.py              # Fachada unificada (Orquestador principal)
│
└── templates/                  # Capa de presentación (Vistas HTML)
    ├── base.html               # Plantilla maestra de la interfaz web
    ├── index.html              # Tablero principal de la aplicación
    ├── candidatos.html         # Visualización y listado de postulantes
    ├── candidato_nuevo.html    # Formulario de alta de candidatos
    ├── busquedas.html          # Panel de vacantes laborales abiertas
    ├── busqueda_nueva.html     # Registro de nuevos puestos de trabajo
    ├── evaluaciones.html       # Módulo de carga de exámenes y puntuaciones
    └── turnos.html
```

## Conceptos de POO implementados

* Clase Usuario (Base/abstracción) Representa la entidad genérica del sistema.
no se instancia, sirve como una plantilla estructural.
* Clase Candidato (Hereeda de Usuario), Maneja polimorfismo ya que extiende o sobreescribe comportamientos especializados que no estan presentes en la clase padre.
* Clase Busqueda y Evaluacion (Asociación/Composición) guarda referencias directas
a instancias vivas de objetos Candidato y Busqueda.
*Las clases dentro del módulo Servicios: Muestran encapsulamiento de lógica, centralizan los métodos públicos con validaciones antes de mutar colecciones.


## Funcionalidades

* Gestión de candidatos
* Gestión de búsquedas laborales
* Evaluaciones
* Agenda de entrevistas
* Dashboard
* Carga automática de datos de demostración

## Persistencia

Actualmente la información se mantiene en memoria durante la ejecución de la aplicación.

## Autores
* Lucía Ayelén Ridao Schelling
* Lorenzo Quintan
* Aaron Ezequiel Busto
=======
# TP-FINAL-PROGRAMACION-UNAB

