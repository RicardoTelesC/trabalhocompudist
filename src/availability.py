"""Fórmulas de disponibilidade para serviço replicado (Exercício 1.1)."""

from __future__ import annotations

import math

from scipy.stats import binom


def availability_general(n: int, k: int, p: float) -> float:
    """
    Disponibilidade analítica: P(X >= k) para X ~ Bin(n, p).

    A(n, k, p) = sum_{i=k}^{n} C(n,i) * p^i * (1-p)^(n-i)
    """
    if not (n > 0 and 0 < k <= n and 0.0 <= p <= 1.0):
        raise ValueError("Requer n > 0, 0 < k <= n e 0 <= p <= 1")

    if p == 0.0:
        return 0.0
    if p == 1.0:
        return 1.0

    # P(X >= k) = 1 - P(X <= k-1)
    return float(1.0 - binom.cdf(k - 1, n, p))


def availability_read(n: int, p: float) -> float:
    """Caso k = 1: A(n, 1, p) = 1 - (1 - p)^n."""
    return 1.0 - (1.0 - p) ** n


def availability_write(n: int, p: float) -> float:
    """Caso k = n: A(n, n, p) = p^n."""
    return p**n


def k_values_for_n(n: int) -> list[tuple[str, int]]:
    """Retorna casos de comparação: k=1, k=⌈n/2⌉, k=n."""
    half = math.ceil(n / 2)
    return [
        ("k=1 (consulta)", 1),
        (f"k=ceil(n/2)={half} (quorum)", half),
        (f"k=n={n} (atualizacao)", n),
    ]
