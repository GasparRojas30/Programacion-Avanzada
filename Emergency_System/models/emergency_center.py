from dataclasses import dataclass

@dataclass
class EmergencyCenter:
    """
    Representa un centro de emergencias el cual recibe incidentes.
    """
    id: str
    nombre: str
    ubicacion: str

def __eq__(self, other: object) -> bool:
        return isinstance(other, EmergencyCenter) and other.id == self.id

def __hash__(self) -> int:
        return hash(self.id)

def __repr__(self) -> str:
        return f"EmergencyCenter(id={self.id}, nombre={self.nombre}, direccion={self.direccion})"



