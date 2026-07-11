from __future__ import annotations

from typing import Any, Callable, List


Key = Callable[[Any], Any]


def _identity(x: Any) -> Any:
    return x

def merge_sort(data: List[Any], key: Key = _identity, reverse: bool = False) -> List[Any]:
    arr = list(data)
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = merge_sort(arr[:mid], key, reverse)
    right = merge_sort(arr[mid:], key, reverse)
    return _merge(left, right, key, reverse)


def _merge(left: List[Any], right: List[Any], key: Key, reverse: bool) -> List[Any]:
    result: List[Any] = []
    i = j = 0
    while i < len(left) and j < len(right):
        lk, rk = key(left[i]), key(right[j])
        take_left = (lk >= rk) if reverse else (lk <= rk)
        if take_left:
            result.append(left[i]); i += 1
        else:
            result.append(right[j]); j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result

def quick_sort(data: List[Any], key: Key = _identity, reverse: bool = False) -> List[Any]:
    """
    pre: `data` es una lista; `key` mapea cada elemento a algo comparable.
    post: retorna una NUEVA lista ordenada; `data` no se modifica.
    """
    arr = list(data)
    _quick_sort(arr, 0, len(arr) - 1, key, reverse)
    return arr


def _quick_sort(arr: List[Any], lo: int, hi: int, key: Key, reverse: bool) -> None:
    while lo < hi:
        p = _partition(arr, lo, hi, key, reverse)
        if p - lo < hi - p:
            _quick_sort(arr, lo, p - 1, key, reverse)
            lo = p + 1
        else:
            _quick_sort(arr, p + 1, hi, key, reverse)
            hi = p - 1


def _partition(arr: List[Any], lo: int, hi: int, key: Key, reverse: bool) -> int:
    mid = (lo + hi) // 2
    _median_of_three(arr, lo, mid, hi, key, reverse)
    arr[mid], arr[hi - 1] = arr[hi - 1], arr[mid]
    pivot = key(arr[hi - 1])

    i = lo
    for j in range(lo, hi - 1):
        cmp = (key(arr[j]) >= pivot) if reverse else (key(arr[j]) <= pivot)
        if cmp:
            arr[i], arr[j] = arr[j], arr[i]
            i += 1
    arr[i], arr[hi - 1] = arr[hi - 1], arr[i]
    return i


def _median_of_three(arr, lo, mid, hi, key, reverse) -> None:
    def less(a, b):
        return (key(a) > key(b)) if reverse else (key(a) < key(b))

    if less(arr[mid], arr[lo]):
        arr[lo], arr[mid] = arr[mid], arr[lo]
    if less(arr[hi], arr[lo]):
        arr[lo], arr[hi] = arr[hi], arr[lo]
    if less(arr[hi], arr[mid]):
        arr[mid], arr[hi] = arr[hi], arr[mid]


def contar_por_zona(incidentes: List[Any]) -> List[tuple[str, int]]:
    """
    Cuenta incidentes por zona y devuelve la lista ordenada de mayor a
    menor frecuencia usando merge_sort (estable).
    """
    conteo: dict[str, int] = {}
    for inc in incidentes:
        conteo[inc.zona] = conteo.get(inc.zona, 0) + 1
    pares = [(zona, n) for zona, n in conteo.items()]
    return merge_sort(pares, key=lambda p: p[1], reverse=True)