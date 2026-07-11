from __future__ import annotations

from typing import Any, Iterator, Optional


class _Entry:
    """Par clave/valor almacenado en un bucket (nodo de la lista enlazada)."""

    __slots__ = ("key", "value", "next")

    def __init__(self, key: str, value: Any, nxt: "Optional[_Entry]" = None) -> None:
        self.key = key
        self.value = value
        self.next = nxt


class HashTable:

    def __init__(self, capacity: int = 16, max_load: float = 0.75) -> None:
        self._capacity = max(4, capacity)
        self._buckets: list[Optional[_Entry]] = [None] * self._capacity
        self._size = 0
        self._max_load = max_load
        self._collisions = 0

    def _hash(self, key: str) -> int:
        h = 5381
        for ch in str(key):
            h = ((h << 5) + h) + ord(ch)  # h * 33 + ord(ch)
            h &= 0xFFFFFFFF               # mantiene 32 bits
        return h % self._capacity

    def insert(self, key: str, value: Any) -> None:
        idx = self._hash(key)
        head = self._buckets[idx]

        node = head
        while node is not None:
            if node.key == key:
                node.value = value
                return
            node = node.next

        if head is not None:
            self._collisions += 1 
        self._buckets[idx] = _Entry(key, value, head)
        self._size += 1

        if self.load_factor() > self._max_load:
            self._resize(self._capacity * 2)

    def search(self, key: str) -> Optional[Any]:
        node = self._buckets[self._hash(key)]
        while node is not None:
            if node.key == key:
                return node.value
            node = node.next
        return None

    def contains(self, key: str) -> bool:
        return self.search(key) is not None

    def delete(self, key: str) -> bool:
        idx = self._hash(key)
        node = self._buckets[idx]
        prev: Optional[_Entry] = None
        while node is not None:
            if node.key == key:
                if prev is None:
                    self._buckets[idx] = node.next
                else:
                    prev.next = node.next
                self._size -= 1
                return True
            prev, node = node, node.next
        return False

    def update_state(self, key: str, new_state: Any) -> bool:
        value = self.search(key)
        if value is None:
            return False
        if hasattr(value, "estado"):
            value.estado = new_state
        return True

    def _resize(self, new_capacity: int) -> None:
        old = self._buckets
        self._capacity = new_capacity
        self._buckets = [None] * new_capacity
        self._size = 0
        self._collisions = 0
        for head in old:
            node = head
            while node is not None:
                self.insert(node.key, node.value)
                node = node.next

    def load_factor(self) -> float:
        return self._size / self._capacity

    def used_buckets(self) -> int:
        return sum(1 for b in self._buckets if b is not None)

    def max_bucket_size(self) -> int:
        peor = 0
        for head in self._buckets:
            length = 0
            node = head
            while node is not None:
                length += 1
                node = node.next
            peor = max(peor, length)
        return peor

    def stats(self) -> dict[str, Any]:
        return {
            "elementos": self._size,
            "capacidad": self._capacity,
            "factor_carga": round(self.load_factor(), 4),
            "colisiones": self._collisions,
            "buckets_utilizados": self.used_buckets(),
            "max_tamano_bucket": self.max_bucket_size(),
        }

    def __len__(self) -> int:
        return self._size

    def __contains__(self, key: str) -> bool:
        return self.contains(key)

    def values(self) -> Iterator[Any]:
        for head in self._buckets:
            node = head
            while node is not None:
                yield node.value
                node = node.next

    def keys(self) -> Iterator[str]:
        for head in self._buckets:
            node = head
            while node is not None:
                yield node.key
                node = node.next