from enum import Enum

class EstadoCandidato(Enum):
    REGISTRADO = "registrado"
    EVALUADO = "evaluado"
    APROBADO = "aprobado"
    RECHAZADO = "rechazado"

class EstadoBusqueda(Enum):
    ABIERTA = "abierta"
    CERRADA = "cerrada"
    EN_REVISION = "en_revision"

class ResultadoEvaluacion(Enum):
    PENDIENTE = "pendiente"
    APROBADO = "aprobado"
    RECHAZADO = "rechazado"

class EstadoTurno(Enum):
    AGENDADO = "agendado"
    COMPLETADO = "completado"
    CANCELADO = "cancelado"
    NO_PRESENTADO = "no_presentado"