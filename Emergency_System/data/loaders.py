from __future__ import annotations
import csv
import os
from datetime import datetime
from ..models.incident import Incident, Priority, IncidentType, IncidentStatus
from ..models.emergency_center import EmergencyCenter
from ..models.road_network import RoadNetwork

DATA_DIR = os.path.dirname(os.path.abspath(__file__))

def load_incidents(path: str | None = None) -> list[Incident]:
    path = path or os.path.join(DATA_DIR, "incidentes.csv")
    out: list[Incident] = []
    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            out.append(Incident(
                id=row["id"],
                zona=row["zona"],
                prioridad=Priority(int(row["prioridad"])),
                tipo=IncidentType(int(row["tipo"])),
                timestamp=datetime.fromisoformat(row["timestamp"]),
                estado=IncidentStatus(int(row.get("estado", 0))),
                severidad=int(row.get("severidad", 1)),
            ))
    return out

def load_centers(path: str | None = None) -> list[EmergencyCenter]:
    path = path or os.path.join(DATA_DIR, "centros.csv")
    out: list[EmergencyCenter] = []
    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            out.append(EmergencyCenter(row["id"], row["nombre"], row["ubicacion"]))
    return out

def load_network(edges_path: str | None = None,
                 nodes_path: str | None = None) -> RoadNetwork:
    edges_path = edges_path or os.path.join(DATA_DIR, "red_vial.csv")
    nodes_path = nodes_path or os.path.join(DATA_DIR, "nodos.csv")
    g = RoadNetwork()
    g.load_csv(edges_path, nodes_path)
    return g