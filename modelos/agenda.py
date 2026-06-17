from datetime import datetime, date, timedelta
from .enums import EstadoTurno
from .empleos import Evaluacion

class Turno:
    """Clase que representa un turno de entrevista - COMPOSICIÓN de Evaluación."""
    
    _contador_ids = 0
    
    def __init__(self, evaluacion: Evaluacion, fecha: date, hora: str,
                 entrevistador: str, sala: str):
        self._id = self._generar_id()
        self._evaluacion = evaluacion
        self._fecha = fecha
        self._hora = hora
        self._entrevistador = entrevistador
        self._sala = sala
        self._estado = EstadoTurno.AGENDADO
        self._observaciones = ""
        self._fecha_creacion = datetime.now()
        self._fecha_cancelacion = None
    
    @staticmethod
    def _generar_id() -> int:
        Turno._contador_ids += 1
        return Turno._contador_ids
    
    @property
    def id(self) -> int: return self._id
    @property
    def evaluacion(self) -> Evaluacion: return self._evaluacion
    @property
    def fecha(self) -> date: return self._fecha
    @property
    def hora(self) -> str: return self._hora
    @property
    def entrevistador(self) -> str: return self._entrevistador
    @property
    def sala(self) -> str: return self._sala
    @property
    def estado(self) -> EstadoTurno: return self._estado
    @property
    def observaciones(self) -> str: return self._observaciones
    
    @entrevistador.setter
    def entrevistador(self, nuevo_entrevistador: str):
        if self._estado == EstadoTurno.AGENDADO: self._entrevistador = nuevo_entrevistador
    
    @sala.setter
    def sala(self, nueva_sala: str):
        if self._estado == EstadoTurno.AGENDADO: self._sala = nueva_sala
    
    def agendar(self) -> bool: return self._estado == EstadoTurno.AGENDADO
    
    def cancelar(self, motivo: str = "") -> bool:
        if self._estado in [EstadoTurno.COMPLETADO, EstadoTurno.CANCELADO]: return False
        self._estado = EstadoTurno.CANCELADO
        self._observaciones = motivo
        self._fecha_cancelacion = datetime.now()
        return True
    
    def completar(self, observaciones: str = "") -> bool:
        if self._estado != EstadoTurno.AGENDADO: return False
        self._estado = EstadoTurno.COMPLETADO
        self._observaciones = observaciones
        return True
    
    def es_disponible(self) -> bool: return self._estado == EstadoTurno.AGENDADO
    def es_futuro(self) -> bool: return self._fecha >= date.today()
    
    def obtener_datos_candidato(self) -> dict:
        cand = self._evaluacion.candidato
        return {'id': cand.id, 'nombre': cand.nombre, 'email': cand.email, 'telefono': cand.telefono}
    
    def obtener_datos_puesto(self) -> dict:
        busq = self._evaluacion.busqueda
        return {'id': busq.id, 'titulo': busq.titulo_puesto, 'descripcion': busq.descripcion, 'salario_rango': busq.obtener_rango_salario()}
    
    def obtener_info(self) -> str:
        cand = self._evaluacion.candidato
        busq = self._evaluacion.busqueda
        return f"""
        ═══════════════════════════════════════════
        TURNO DE ENTREVISTA
        ═══════════════════════════════════════════
        ID: {self._id}
        Candidato: {cand.nombre}
        Puesto: {busq.titulo_puesto}
        Fecha: {self._fecha.strftime('%d/%m/%Y')}
        Hora: {self._hora}
        Entrevistador: {self._entrevistador}
        Sala: {self._sala}
        Estado: {self._estado.value}
        Observaciones: {self._observaciones if self._observaciones else 'Sin observaciones'}
        ═══════════════════════════════════════════
        """
    
    def obtener_info_compacta(self) -> dict:
        return {
            'id': self._id, 'evaluacion_id': self._evaluacion.id, 'candidato_nombre': self._evaluacion.candidato.nombre,
            'puesto': self._evaluacion.busqueda.titulo_puesto, 'fecha': self._fecha.isoformat(),
            'hora': self._hora, 'entrevistador': self._entrevistador, 'sala': self._sala,
            'estado': self._estado.value, 'observaciones': self._observaciones, 'fecha_creacion': self._fecha_creacion.isoformat()
        }
    
    def __str__(self) -> str: return f"Turno {self._id}: {self._evaluacion.candidato.nombre} - {self._fecha} {self._hora}"
    def __repr__(self) -> str: return f"Turno(id={self._id}, evaluacion_id={self._evaluacion.id}, fecha={self._fecha}, hora={self._hora})"


class Calendario:
    """Clase que gestiona calendario - AGREGACIÓN de Turnos."""
    
    _contador_ids = 0
    
    def __init__(self, salas_disponibles: list = None):
        self._id = self._generar_id()
        self._horarios_disponibles = {}
        self._turnos_agendados = []
        self._salas_disponibles = salas_disponibles or ["Sala A", "Sala B", "Sala C"]
        self._fecha_inicio_calendario = date.today()
        self._fecha_fin_calendario = date.today() + timedelta(days=90)
        self._inicializar_horarios()
    
    @staticmethod
    def _generar_id() -> int:
        Calendario._contador_ids += 1
        return Calendario._contador_ids
    
    def _inicializar_horarios(self) -> None:
        fecha_actual = self._fecha_inicio_calendario
        while fecha_actual <= self._fecha_fin_calendario:
            if fecha_actual.weekday() < 5:
                fecha_str = fecha_actual.strftime('%Y-%m-%d')
                horarios = self._generar_slots_horarios()
                self._horarios_disponibles[fecha_str] = horarios
            fecha_actual += timedelta(days=1)
    
    def _generar_slots_horarios(self) -> list:
        horarios = []
        hora_inicio = datetime.combine(date.today(), datetime.min.time().replace(hour=9))
        hora_fin = datetime.combine(date.today(), datetime.min.time().replace(hour=17))
        while hora_inicio <= hora_fin:
            horarios.append(hora_inicio.strftime('%H:%M'))
            hora_inicio += timedelta(minutes=30)
        return horarios
    
    @property
    def id(self) -> int: return self._id
    @property
    def turnos_agendados(self) -> list: return self._turnos_agendados.copy()
    @property
    def salas_disponibles(self) -> list: return self._salas_disponibles.copy()
    
    def obtener_slots_libres(self, fecha: str) -> list:
        if fecha not in self._horarios_disponibles: return []
        horarios_libres = self._horarios_disponibles[fecha].copy()
        for turno in self._turnos_agendados:
            if turno.fecha.strftime('%Y-%m-%d') == fecha:
                if turno.hora in horarios_libres:
                    horarios_libres.remove(turno.hora)
        return horarios_libres
    
    def esta_disponible(self, fecha: str, hora: str) -> bool:
        return hora in self.obtener_slots_libres(fecha)
    
    def agregar_turno(self, turno: Turno) -> bool:
        fecha_str = turno.fecha.strftime('%Y-%m-%d')
        if self.esta_disponible(fecha_str, turno.hora):
            self._turnos_agendados.append(turno)
            return True
        return False
    
    def eliminar_turno(self, turno: Turno) -> bool:
        if turno in self._turnos_agendados:
            self._turnos_agendados.remove(turno)
            return True
        return False
    
    def obtener_turnos_proximos(self, cantidad: int = 10) -> list:
        turnos_futuros = [t for t in self._turnos_agendados if t.es_futuro()]
        turnos_ordenados = sorted(turnos_futuros, key=lambda x: (x.fecha, x.hora))
        return turnos_ordenados[:cantidad]
    
    def obtener_info(self) -> str:
        return f"""
        ═══════════════════════════════════════════
        CALENDARIO
        ═══════════════════════════════════════════
        ID: {self._id}
        Período: {self._fecha_inicio_calendario} a {self._fecha_fin_calendario}
        Salas disponibles: {', '.join(self._salas_disponibles)}
        Turnos agendados: {len(self._turnos_agendados)}
        ═══════════════════════════════════════════
        """