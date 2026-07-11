from dataclasses import dataclass, field
from datetime import datetime
from enum import IntEnum

class Priority(IntEnum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4

class IncidentStatus(IntEnum):
    REPORTED = 0
    ASSIGNED = 1
    IN_PROGRESS = 2
    RESOLVED = 3

class IncidentType(IntEnum):
    MEDICAL = 0
    FIRE = 1
    RESCUE = 2
    STRUCTURAL = 3

@dataclass
class Incident:
    """
    Representa un incidente el cual se reporta al sistema de emergencias.
    """
    id: str
    zona: str
    prioridad: Priority
    tipo: IncidentType
    timestamp: datetime
    estado: IncidentStatus = IncidentStatus.REPORTED
    severidad: int = 1

    def score(self, now: datetime) -> float:
        """
        Calcula la prioridad del incidente
        pre: now >= self.timestamp
        post: retorna severidad * factor de tiempo, mayor severidad = mas urgente
        """
        minutos = max((now - self.timestamp).total_seconds() / 60, 1)
        factor_tiempo = 1 / (minutos / 60)
        return self.severidad * int(self.prioridad) * factor_tiempo