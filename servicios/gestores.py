from datetime import date
from modelos.usuarios import Candidato
from modelos.empleos import Busqueda, Evaluacion
from modelos.agenda import Turno, Calendario

class ServicioCandidato:
    def __init__(self):
        self._candidatos = []
    
    def registrar_candidato(self, candidato: Candidato) -> bool:
        if not candidato.validar():
            print("Error: Los datos del candidato no son válidos")
            return False
        self._candidatos.append(candidato)
        return True
    
    def obtener_candidato_por_id(self, candidato_id: int):
        for c in self._candidatos:
            if c.id == candidato_id: return c
        return None
    
    def obtener_todos_candidatos(self) -> list: return self._candidatos.copy()
    
    def generar_reporte_candidatos(self) -> dict:
        total = len(self._candidatos)
        registrados = len([c for c in self._candidatos if c.estado.value == 'registrado'])
        aprobados = len([c for c in self._candidatos if c.estado.value == 'aprobado'])
        rechazados = len([c for c in self._candidatos if c.estado.value == 'rechazado'])
        return {'total_candidatos': total, 'registrados': registrados, 'aprobados': aprobados, 'rechazados': rechazados}

class ServicioEvaluacion:
    def __init__(self):
        self._evaluaciones = []
    
    def crear_evaluacion(self, candidato: Candidato, busqueda: Busqueda, evaluador: str) -> Evaluacion:
        evaluacion = Evaluacion(candidato, busqueda, evaluador)
        self._evaluaciones.append(evaluacion)
        return evaluacion
    
    def evaluar_candidato(self, evaluacion: Evaluacion, resultado: str, puntuacion: float, comentarios: str = "") -> bool:
        try:
            return evaluacion.evaluar(resultado, puntuacion, comentarios)
        except ValueError as e:
            print(f"Error al evaluar: {e}")
            return False
    
    def obtener_evaluaciones_aprobadas(self) -> list:
        return [e for e in self._evaluaciones if e.es_aprobado()]
    
    def obtener_todas_evaluaciones(self) -> list: return self._evaluaciones.copy()
    
    def generar_reporte_evaluaciones(self) -> dict:
        total = len(self._evaluaciones)
        aprobadas = len(self.obtener_evaluaciones_aprobadas())
        rechazadas = len([e for e in self._evaluaciones if e.es_rechazado()])
        porcentaje_aprobacion = (aprobadas / total * 100) if total > 0 else 0
        return {'total_evaluaciones': total, 'aprobadas': aprobadas, 'rechazadas': rechazadas, 'tasa_aprobacion': round(porcentaje_aprobacion, 2)}

class ServicioCalendario:
    def __init__(self, calendario: Calendario):
        self._calendario = calendario
        self._turnos = []
    
    def crear_turno(self, evaluacion: Evaluacion, fecha: date, hora: str, entrevistador: str, sala: str):
        if not evaluacion.es_aprobado():
            print("Error: Solo se pueden agendar turnos para candidatos aprobados")
            return None
        
        fecha_str = fecha.strftime('%Y-%m-%d')
        if not self._calendario.esta_disponible(fecha_str, hora):
            print(f"Error: El slot {fecha_str} {hora} no está disponible")
            return None
        
        turno = Turno(evaluacion, fecha, hora, entrevistador, sala)
        if self._calendario.agregar_turno(turno):
            self._turnos.append(turno)
            return turno
        else:
            print("Error: No se pudo agregar el turno al calendario")
            return None
    
    def cancelar_turno(self, turno_id: int, motivo: str = "") -> bool:
        turno = self.obtener_turno_por_id(turno_id)
        if not turno:
            print(f"Error: Turno {turno_id} no encontrado")
            return False
        if turno.cancelar(motivo):
            self._calendario.eliminar_turno(turno)
            return True
        return False
    
    def obtener_turno_por_id(self, turno_id: int):
        for t in self._turnos:
            if t.id == turno_id: return t
        return None
    
    def obtener_turnos_proximos(self, cantidad: int = 10) -> list:
        turnos_futuros = [t for t in self._turnos if t.es_futuro() and t.es_disponible()]
        turnos_ordenados = sorted(turnos_futuros, key=lambda x: (x.fecha, x.hora))
        return turnos_ordenados[:cantidad]
    
    def obtener_todos_turnos(self) -> list: return self._turnos.copy()
    
    def generar_reporte_turnos(self) -> dict:
        total = len(self._turnos)
        agendados = len([t for t in self._turnos if t.es_disponible()])
        completados = len([t for t in self._turnos if t.estado.value == 'completado'])
        cancelados = len([t for t in self._turnos if t.estado.value == 'cancelado'])
        return {'total_turnos': total, 'agendados': agendados, 'completados': completados, 'cancelados': cancelados}