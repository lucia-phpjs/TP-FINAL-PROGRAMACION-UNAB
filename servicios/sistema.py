from datetime import datetime
from modelos.usuarios import Candidato, EstadoCandidato
from modelos.empleos import Busqueda, Evaluacion
from modelos.agenda import Turno, Calendario
from .gestores import ServicioCandidato, ServicioEvaluacion, ServicioCalendario

class SistemaEntrevistas:
    """Clase principal que orquesta todo el sistema."""
    
    def __init__(self):
        self._calendario = Calendario()
        self._servicio_evaluacion = ServicioEvaluacion()
        self._servicio_calendario = ServicioCalendario(self._calendario)
        self._servicio_candidato = ServicioCandidato()
        self._candidatos = []
        self._busquedas = []
    
    def registrar_candidato(self, nombre: str, email: str, telefono: str, anos_experiencia: int, cv: str) -> Candidato:
        try:
            candidato = Candidato(nombre, email, telefono, anos_experiencia, cv)
            if self._servicio_candidato.registrar_candidato(candidato):
                self._candidatos.append(candidato)
                print(f"✅ Candidato '{nombre}' registrado exitosamente")
                return candidato
        except ValueError as e:
            print(f"❌ Error: {e}")
        return None
    
    def crear_busqueda(self, titulo: str, descripcion: str, salario_min: float, salario_max: float, skills: list, exp_min: int) -> Busqueda:
        busqueda = Busqueda(titulo, descripcion, salario_min, salario_max, skills, exp_min)
        self._busquedas.append(busqueda)
        print(f"✅ Búsqueda '{titulo}' creada exitosamente")
        return busqueda
    
    def evaluar_candidato(self, candidato_id: int, busqueda_id: int, evaluador: str, resultado: str, puntuacion: float, comentarios: str = "") -> Evaluacion:
        candidato = next((c for c in self._candidatos if c.id == candidato_id), None)
        busqueda = next((b for b in self._busquedas if b.id == busqueda_id), None)
        
        if not candidato or not busqueda:
            print("❌ Error: Candidato o búsqueda no encontrados")
            return None
        
        evaluacion = self._servicio_evaluacion.crear_evaluacion(candidato, busqueda, evaluador)
        
        if self._servicio_evaluacion.evaluar_candidato(evaluacion, resultado, puntuacion, comentarios):
            if resultado.lower() == "aprobado":
                candidato.estado = EstadoCandidato.APROBADO
            else:
                candidato.estado = EstadoCandidato.RECHAZADO
            
            print(f"✅ Evaluación guardada: {resultado}")
            return evaluacion
        return None
    
    def agendar_turno(self, evaluacion_id: int, fecha: str, hora: str, entrevistador: str, sala: str) -> Turno:
        evaluacion = next((e for e in self._servicio_evaluacion.obtener_todas_evaluaciones() if e.id == evaluacion_id), None)
        if not evaluacion:
            print("❌ Evaluación no encontrada")
            return None
        
        try:
            fecha_obj = datetime.strptime(fecha, '%Y-%m-%d').date()
            turno = self._servicio_calendario.crear_turno(evaluacion, fecha_obj, hora, entrevistador, sala)
            if turno:
                print(f"✅ Turno agendado para {fecha} a las {hora}")
                return turno
        except ValueError:
            print("❌ Formato de fecha inválido (usar YYYY-MM-DD)")
        return None
    
    def generar_reportes(self):
        print("\n" + "="*60)
        print("REPORTES DEL SISTEMA")
        print("="*60)
        
        rep_cand = self._servicio_candidato.generar_reporte_candidatos()
        print("\n📋 CANDIDATOS")
        for clave, valor in rep_cand.items(): print(f"  {clave}: {valor}")
        
        rep_eval = self._servicio_evaluacion.generar_reporte_evaluaciones()
        print("\n📋 EVALUACIONES")
        for clave, valor in rep_eval.items(): print(f"  {clave}: {valor}")
        
        rep_turn = self._servicio_calendario.generar_reporte_turnos()
        print("\n📋 TURNOS")
        for clave, valor in rep_turn.items(): print(f"  {clave}: {valor}")