"""Simulador estocástico de disponibilidade (Exercício 1.2 — parte 2)."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from .availability import availability_general, k_values_for_n


def simulate_availability(
    n: int,
    k: int,
    p: float,
    rounds: int,
    seed: int | None = None,
) -> float:
    """
    Simula 'rounds' rodadas e retorna a frequência experimental de disponibilidade.

    Em cada rodada, cada um dos n servidores fica disponível com probabilidade p.
    O serviço opera se ao menos k servidores estão disponíveis.
    """
    rng = np.random.default_rng(seed)
    successes = 0

    for _ in range(rounds):
        available = rng.random(n) <= p
        if available.sum() >= k:
            successes += 1

    return successes / rounds


def build_simulation_table(
    n_values: list[int],
    p_values: list[float],
    rounds: int,
    seed: int = 42,
) -> pd.DataFrame:
    """Compara disponibilidade analítica e experimental lado a lado."""
    rows: list[dict] = []

    for n in n_values:
        for label, k in k_values_for_n(n):
            for p in p_values:
                analytical = availability_general(n, k, p)
                experimental = simulate_availability(n, k, p, rounds, seed=seed)
                rows.append(
                    {
                        "n": n,
                        "k": k,
                        "caso": label,
                        "p": p,
                        "disponibilidade_analitica": analytical,
                        "disponibilidade_experimental": experimental,
                        "diferenca_absoluta": abs(analytical - experimental),
                        "rodadas": rounds,
                    }
                )

    return pd.DataFrame(rows)


def plot_analytical_vs_experimental(
    table: pd.DataFrame,
    output_dir: Path,
) -> Path:
    """Gráfico 2D comparando valores analíticos e experimentais."""
    fig, ax = plt.subplots(figsize=(8, 8))

    x = table["disponibilidade_analitica"]
    y = table["disponibilidade_experimental"]
    ax.scatter(x, y, alpha=0.7, edgecolors="k", linewidths=0.5)

    lims = [0, 1]
    ax.plot(lims, lims, "r--", linewidth=1.5, label="y = x (concordância perfeita)")
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_xlabel("Disponibilidade analítica")
    ax.set_ylabel("Disponibilidade experimental")
    ax.set_title("Teoria vs. Simulação")
    ax.grid(True, alpha=0.3)
    ax.legend()
    ax.set_aspect("equal")
    fig.tight_layout()

    path = output_dir / "simulacao_analitico_vs_experimental.png"
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    return path


def plot_convergence(
    n: int,
    k: int,
    p: float,
    max_rounds: int,
    output_dir: Path,
    seed: int = 42,
) -> Path:
    """Mostra convergência da estimativa experimental para o valor analítico."""
    rng = np.random.default_rng(seed)
    analytical = availability_general(n, k, p)

    cumulative_success = 0
    estimates: list[float] = []
    checkpoints = np.unique(
        np.logspace(1, np.log10(max_rounds), 50, dtype=int)
    )

    for r in range(1, max_rounds + 1):
        available = rng.random(n) <= p
        if available.sum() >= k:
            cumulative_success += 1
        if r in checkpoints:
            estimates.append(cumulative_success / r)

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.semilogx(checkpoints, estimates, "b-o", markersize=4, label="Estimativa experimental")
    ax.axhline(analytical, color="r", linestyle="--", linewidth=2, label=f"Analítico = {analytical:.4f}")
    ax.set_xlabel("Número de rodadas")
    ax.set_ylabel("Disponibilidade estimada")
    ax.set_title(f"Convergência da simulação (n={n}, k={k}, p={p})")
    ax.grid(True, alpha=0.3, which="both")
    ax.legend()
    fig.tight_layout()

    path = output_dir / f"simulacao_convergencia_n{n}_k{k}_p{int(p*100)}.png"
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    return path


def run_simulation(output_dir: Path, rounds: int = 100_000) -> pd.DataFrame:
    """Executa simulação completa e salva resultados."""
    output_dir.mkdir(parents=True, exist_ok=True)

    n_values = [1, 2, 3, 5, 10]
    p_values = [0.5, 0.7, 0.9, 0.95, 0.99]

    table = build_simulation_table(n_values, p_values, rounds)
    csv_path = output_dir / "simulacao_tabela.csv"
    table.to_csv(csv_path, index=False, float_format="%.6f")

    plot_analytical_vs_experimental(table, output_dir)
    plot_convergence(n=5, k=1, p=0.9, max_rounds=rounds, output_dir=output_dir)
    plot_convergence(n=5, k=5, p=0.9, max_rounds=rounds, output_dir=output_dir)

    print(f"[Simulação] Tabela salva em: {csv_path}")
    print(f"[Simulação] Diferença média absoluta: {table['diferenca_absoluta'].mean():.6f}")
    return table
