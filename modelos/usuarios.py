from abc import ABC, abstractmethod
from datetime import datetime
import re
from .enums import EstadoCandidato

class Persona(ABC):
    """Clase abstracta base que representa a una persona en el sistema."""
    
    _contador_ids = 0
    
    def __init__(self, nombre: str, email: str, telefono: str):
        self._id = self._generar_id()
        self._nombre = nombre
        self._email = email if self._validar_email(email) else None
        self._telefono = telefono
        self._fecha_registro = datetime.now()
        
        if self._email is None:
            raise ValueError(f"Email inválido: {email}")
    
    @staticmethod
    def _generar_id() -> int:
        Persona._contador_ids += 1
        return Persona._contador_ids
    
    @staticmethod
    def _validar_email(email: str) -> bool:
        patron = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(patron, email) is not None
    
    @property
    def id(self) -> int: return self._id
    @property
    def nombre(self) -> str: return self._nombre
    @property
    def email(self) -> str: return self._email
    @property
    def telefono(self) -> str: return self._telefono
    @property
    def fecha_registro(self) -> datetime: return self._fecha_registro
    
    @email.setter
    def email(self, nuevo_email: str):
        if self._validar_email(nuevo_email):
            self._email = nuevo_email
        else:
            raise ValueError(f"Email inválido: {nuevo_email}")
    
    @abstractmethod
    def obtener_info(self) -> str: pass
    
    @abstractmethod
    def validar(self) -> bool: pass
    
    def obtener_contacto(self) -> dict:
        return {'email': self._email, 'telefono': self._telefono}
    
    def __str__(self) -> str: return self.obtener_info()
    def __repr__(self) -> str: return f"Persona(id={self._id}, nombre='{self._nombre}', email='{self._email}')"


class Candidato(Persona):
    """Clase que representa un candidato - Hereda de Persona."""
    
    def __init__(self, nombre: str, email: str, telefono: str, 
                 anos_experiencia: int, cv: str):
        super().__init__(nombre, email, telefono)
        self._anos_experiencia = anos_experiencia
        self._habilidades = []
        self._cv = cv
        self._estado = EstadoCandidato.REGISTRADO
        self._fecha_postulacion = datetime.now()
    
    @property
    def anos_experiencia(self) -> int: return self._anos_experiencia
    @property
    def habilidades(self) -> list: return self._habilidades.copy()
    @property
    def cv(self) -> str: return self._cv
    @property
    def estado(self) -> EstadoCandidato: return self._estado
    @property
    def fecha_postulacion(self) -> datetime: return self._fecha_postulacion
    
    @anos_experiencia.setter
    def anos_experiencia(self, anos: int):
        if anos < 0: raise ValueError("Los años de experiencia no pueden ser negativos")
        self._anos_experiencia = anos
    
    @cv.setter
    def cv(self, nuevo_cv: str): self._cv = nuevo_cv
    @estado.setter
    def estado(self, nuevo_estado: EstadoCandidato): self._estado = nuevo_estado
    
    def agregar_habilidad(self, habilidad: str) -> None:
        if habilidad and habilidad not in self._habilidades:
            self._habilidades.append(habilidad)
    
    def agregar_multiples_habilidades(self, habilidades: list) -> None:
        for habilidad in habilidades:
            self.agregar_habilidad(habilidad)
    
    def eliminar_habilidad(self, habilidad: str) -> bool:
        if habilidad in self._habilidades:
            self._habilidades.remove(habilidad)
            return True
        return False
    
    def tiene_experiencia_minima(self, anos_minimos: int) -> bool:
        return self._anos_experiencia >= anos_minimos
    
    def tiene_habilidad(self, habilidad: str) -> bool:
        return habilidad.lower() in [h.lower() for h in self._habilidades]
    
    def tiene_todas_habilidades(self, habilidades_requeridas: list) -> bool:
        for habilidad in habilidades_requeridas:
            if not self.tiene_habilidad(habilidad): return False
        return True
    
    def obtener_info(self) -> str:
        return f"""
        ═══════════════════════════════════════════
        DATOS DEL CANDIDATO
        ═══════════════════════════════════════════
        ID: {self._id}
        Nombre: {self._nombre}
        Email: {self._email}
        Teléfono: {self._telefono}
        Experiencia: {self._anos_experiencia} años
        Estado: {self._estado.value}
        Habilidades: {', '.join(self._habilidades) if self._habilidades else 'Sin habilidades'}
        Fecha de postulación: {self._fecha_postulacion.strftime('%d/%m/%Y %H:%M')}
        ═══════════════════════════════════════════
        """
    
    def validar(self) -> bool:
        validaciones = {
            'nombre_valido': len(self._nombre.strip()) > 0,
            'email_valido': self._email is not None,
            'telefono_valido': len(self._telefono.strip()) > 0,
            'experiencia_valida': self._anos_experiencia >= 0,
            'cv_valido': len(self._cv.strip()) > 0
        }
        return all(validaciones.values())
    
    def obtener_info_compacta(self) -> dict:
        return {
            'id': self._id, 'nombre': self._nombre, 'email': self._email,
            'telefono': self._telefono, 'anos_experiencia': self._anos_experiencia,
            'habilidades': self._habilidades.copy(), 'estado': self._estado.value,
            'fecha_postulacion': self._fecha_postulacion.isoformat()
        }
    
    def __str__(self) -> str: return f"{self._nombre} ({self._anos_experiencia} años exp, {self._estado.value})"
    def __repr__(self) -> str: return f"Candidato(id={self._id}, nombre='{self._nombre}', exp={self._anos_experiencia})"