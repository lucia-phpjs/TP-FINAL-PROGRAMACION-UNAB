from datetime import datetime
from .enums import EstadoBusqueda, ResultadoEvaluacion
from .usuarios import Candidato

class Busqueda:
    """Clase que representa una búsqueda de empleo."""
    
    _contador_ids = 0
    
    def __init__(self, titulo_puesto: str, descripcion: str,
                 salario_min: float, salario_max: float,
                 skills_requeridos: list, experiencia_minima: int):
        self._id = self._generar_id()
        self._titulo_puesto = titulo_puesto
        self._descripcion = descripcion
        self._salario_min = salario_min
        self._salario_max = salario_max
        self._skills_requeridos = skills_requeridos.copy()
        self._experiencia_minima = experiencia_minima
        self._estado = EstadoBusqueda.ABIERTA
        self._fecha_creacion = datetime.now()
        self._fecha_cierre = None
    
    @staticmethod
    def _generar_id() -> int:
        Busqueda._contador_ids += 1
        return Busqueda._contador_ids
    
    @property
    def id(self) -> int: return self._id
    @property
    def titulo_puesto(self) -> str: return self._titulo_puesto
    @property
    def descripcion(self) -> str: return self._descripcion
    @property
    def salario_min(self) -> float: return self._salario_min
    @property
    def salario_max(self) -> float: return self._salario_max
    @property
    def skills_requeridos(self) -> list: return self._skills_requeridos.copy()
    @property
    def experiencia_minima(self) -> int: return self._experiencia_minima
    @property
    def estado(self) -> EstadoBusqueda: return self._estado
    
    @estado.setter
    def estado(self, nuevo_estado: EstadoBusqueda):
        self._estado = nuevo_estado
        if nuevo_estado == EstadoBusqueda.CERRADA:
            self._fecha_cierre = datetime.now()
    
    def obtener_requisitos(self) -> dict:
        return {
            'titulo': self._titulo_puesto, 'experiencia_minima': self._experiencia_minima,
            'skills': self._skills_requeridos.copy(), 'salario_rango': f"${self._salario_min} - ${self._salario_max}"
        }
    
    def candidato_cumple_requisitos(self, candidato: Candidato) -> dict:
        cumple_experiencia = candidato.tiene_experiencia_minima(self._experiencia_minima)
        tiene_skills = candidato.tiene_todas_habilidades(self._skills_requeridos)
        skills_faltantes = [s for s in self._skills_requeridos if not candidato.tiene_habilidad(s)]
        
        return {
            'cumple_experiencia': cumple_experiencia, 'cumple_skills': tiene_skills,
            'cumple_todos': cumple_experiencia and tiene_skills, 'skills_faltantes': skills_faltantes,
            'experiencia_candidato': candidato.anos_experiencia, 'experiencia_requerida': self._experiencia_minima
        }
    
    def cerrar_busqueda(self) -> None: self.estado = EstadoBusqueda.CERRADA
    def obtener_rango_salario(self) -> str: return f"${self._salario_min:,.2f} - ${self._salario_max:,.2f}"
    
    def obtener_info(self) -> str:
        return f"""
        ═══════════════════════════════════════════
        BÚSQUEDA DE EMPLEO
        ═══════════════════════════════════════════
        ID: {self._id}
        Puesto: {self._titulo_puesto}
        Estado: {self._estado.value}
        Descripción: {self._descripcion}
        Experiencia mínima: {self._experiencia_minima} años
        Rango salarial: {self.obtener_rango_salario()}
        Skills requeridos: {', '.join(self._skills_requeridos)}
        Fecha creación: {self._fecha_creacion.strftime('%d/%m/%Y %H:%M')}
        ═══════════════════════════════════════════
        """
    
    def obtener_info_compacta(self) -> dict:
        return {
            'id': self._id, 'titulo_puesto': self._titulo_puesto, 'descripcion': self._descripcion,
            'salario_min': self._salario_min, 'salario_max': self._salario_max,
            'skills_requeridos': self._skills_requeridos.copy(), 'experiencia_minima': self._experiencia_minima,
            'estado': self._estado.value, 'fecha_creacion': self._fecha_creacion.isoformat()
        }
    
    def __str__(self) -> str: return f"{self._titulo_puesto} (ID: {self._id}, Estado: {self._estado.value})"
    def __repr__(self) -> str: return f"Busqueda(id={self._id}, titulo='{self._titulo_puesto}')"


class Evaluacion:
    """Clase que representa una evaluación - COMPOSICIÓN de Candidato + Búsqueda."""
    
    _contador_ids = 0
    
    def __init__(self, candidato: Candidato, busqueda: Busqueda, evaluador: str):
        self._id = self._generar_id()
        self._candidato = candidato
        self._busqueda = busqueda
        self._evaluador = evaluador
        self._resultado = ResultadoEvaluacion.PENDIENTE
        self._puntuacion = 0.0
        self._comentarios = ""
        self._fecha_evaluacion = None
    
    @staticmethod
    def _generar_id() -> int:
        Evaluacion._contador_ids += 1
        return Evaluacion._contador_ids
    
    @property
    def id(self) -> int: return self._id
    @property
    def candidato(self) -> Candidato: return self._candidato
    @property
    def busqueda(self) -> Busqueda: return self._busqueda
    @property
    def evaluador(self) -> str: return self._evaluador
    @property
    def resultado(self) -> ResultadoEvaluacion: return self._resultado
    @property
    def puntuacion(self) -> float: return self._puntuacion
    @property
    def comentarios(self) -> str: return self._comentarios
    @property
    def fecha_evaluacion(self) -> datetime: return self._fecha_evaluacion
    
    def evaluar(self, resultado: str, puntuacion: float, comentarios: str = "") -> bool:
        if puntuacion < 0 or puntuacion > 100:
            raise ValueError("La puntuación debe estar entre 0 y 100")
        
        if resultado.lower() == "aprobado":
            self._resultado = ResultadoEvaluacion.APROBADO
        elif resultado.lower() == "rechazado":
            self._resultado = ResultadoEvaluacion.RECHAZADO
        else:
            raise ValueError("Resultado debe ser 'aprobado' o 'rechazado'")
        
        self._puntuacion = puntuacion
        self._comentarios = comentarios
        self._fecha_evaluacion = datetime.now()
        return True
    
    def es_aprobado(self) -> bool: return self._resultado == ResultadoEvaluacion.APROBADO
    def es_rechazado(self) -> bool: return self._resultado == ResultadoEvaluacion.RECHAZADO
    def esta_pendiente(self) -> bool: return self._resultado == ResultadoEvaluacion.PENDIENTE
    
    def obtener_analisis(self) -> dict:
        analisis_requisitos = self._busqueda.candidato_cumple_requisitos(self._candidato)
        return {
            'candidato_nombre': self._candidato.nombre, 'puesto': self._busqueda.titulo_puesto,
            'resultado': self._resultado.value, 'puntuacion': self._puntuacion,
            'cumple_requisitos': analisis_requisitos['cumple_todos'],
            'cumple_experiencia': analisis_requisitos['cumple_experiencia'],
            'cumple_skills': analisis_requisitos['cumple_skills'],
            'skills_faltantes': analisis_requisitos['skills_faltantes'],
            'comentarios': self._comentarios, 'evaluador': self._evaluador,
            'fecha': self._fecha_evaluacion.strftime('%d/%m/%Y %H:%M') if self._fecha_evaluacion else "Pendiente"
        }
    
    def obtener_info(self) -> str:
        return f"""
        ═══════════════════════════════════════════
        EVALUACIÓN
        ═══════════════════════════════════════════
        ID: {self._id}
        Candidato: {self._candidato.nombre}
        Puesto: {self._busqueda.titulo_puesto}
        Evaluador: {self._evaluador}
        Resultado: {self._resultado.value}
        Puntuación: {self._puntuacion}/100
        Comentarios: {self._comentarios if self._comentarios else 'Sin comentarios'}
        Fecha: {self._fecha_evaluacion.strftime('%d/%m/%Y %H:%M') if self._fecha_evaluacion else 'Pendiente'}
        ═══════════════════════════════════════════
        """
    
    def obtener_info_compacta(self) -> dict:
        return {
            'id': self._id, 'candidato_id': self._candidato.id, 'candidato_nombre': self._candidato.nombre,
            'busqueda_id': self._busqueda.id, 'puesto': self._busqueda.titulo_puesto,
            'evaluador': self._evaluador, 'resultado': self._resultado.value, 'puntuacion': self._puntuacion,
            'comentarios': self._comentarios, 'fecha_evaluacion': self._fecha_evaluacion.isoformat() if self._fecha_evaluacion else None
        }
    
    def __str__(self) -> str: return f"Evaluación {self._id}: {self._candidato.nombre} para {self._busqueda.titulo_puesto} - {self._resultado.value}"
    def __repr__(self) -> str: return f"Evaluacion(id={self._id}, candidato_id={self._candidato.id}, busqueda_id={self._busqueda.id})"