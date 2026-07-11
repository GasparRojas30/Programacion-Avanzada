from __future__ import annotations

from typing import Any, Optional

from .hash_table import HashTable


class _PQEntry:
    """Entrada del heap: prioridad (float) + carga util + clave estable."""

    __slots__ = ("priority", "item", "key")

    def __init__(self, priority: float, item: Any, key: str) -> None:
        self.priority = priority
        self.item = item
        self.key = key


class PriorityQueue:
    
    def __init__(self) -> None:
        self._heap: list[_PQEntry] = []
        self._pos = HashTable()  # id -> indice actual en el heap

    def _key(self, item: Any, key: Optional[str]) -> str:
        return key if key is not None else str(getattr(item, "id"))

    def _swap(self, i: int, j: int) -> None:
        self._heap[i], self._heap[j] = self._heap[j], self._heap[i]
        self._pos.insert(self._heap[i].key, i)
        self._pos.insert(self._heap[j].key, j)

    def _sift_up(self, i: int) -> None:
        while i > 0:
            parent = (i - 1) // 2
            if self._heap[i].priority > self._heap[parent].priority:
                self._swap(i, parent)
                i = parent
            else:
                break

    def _sift_down(self, i: int) -> None:
        n = len(self._heap)
        while True:
            largest = i
            left, right = 2 * i + 1, 2 * i + 2
            if left < n and self._heap[left].priority > self._heap[largest].priority:
                largest = left
            if right < n and self._heap[right].priority > self._heap[largest].priority:
                largest = right
            if largest == i:
                break
            self._swap(i, largest)
            i = largest

    def push(self, item: Any, priority: float, key: Optional[str] = None) -> None:
        """Inserta un incidente con su prioridad. O(log n)."""
        k = self._key(item, key)
        if self._pos.contains(k):
            self.update_priority(k, priority)
            return
        self._heap.append(_PQEntry(priority, item, k))
        idx = len(self._heap) - 1
        self._pos.insert(k, idx)
        self._sift_up(idx)

    def pop(self) -> Optional[Any]:
        """Extrae y retorna el incidente MAS URGENTE. O(log n)."""
        if not self._heap:
            return None
        top = self._heap[0]
        last = self._heap.pop()
        self._pos.delete(top.key)
        if self._heap:
            self._heap[0] = last
            self._pos.insert(last.key, 0)
            self._sift_down(0)
        return top.item

    def peek(self) -> Optional[Any]:
        """Retorna (sin extraer) el incidente mas urgente. O(1)."""
        return self._heap[0].item if self._heap else None

    def update_priority(self, key: str, new_priority: float) -> bool:
        """
        Actualiza la prioridad del incidente identificado por `key`.
        Retorna True si existia. O(log n).
        """
        idx = self._pos.search(key)
        if idx is None:
            return False
        old = self._heap[idx].priority
        self._heap[idx].priority = new_priority
        if new_priority > old:
            self._sift_up(idx)
        else:
            self._sift_down(idx)
        return True

    def top_k(self, k: int) -> list[Any]:
        """
        Retorna los k incidentes mas urgentes SIN vaciar la cola.
        O(k log n).
        """
        if k <= 0 or not self._heap:
            return []
        clone = PriorityQueue()
        clone._heap = [_PQEntry(e.priority, e.item, e.key) for e in self._heap]
        for i, e in enumerate(clone._heap):
            clone._pos.insert(e.key, i)
        out = []
        for _ in range(min(k, len(clone._heap))):
            out.append(clone.pop())
        return out

    def __len__(self) -> int:
        return len(self._heap)

    def is_empty(self) -> bool:
        return not self._heap