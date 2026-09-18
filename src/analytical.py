"""Análise analítica de disponibilidade (Exercício 1.2 — parte 1)."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from .availability import availability_general, k_values_for_n


def build_comparison_table(
    n_values: list[int],
    p_values: list[float],
) -> pd.DataFrame:
    """Tabela com disponibilidade analítica para k=1, ⌈n/2⌉ e n."""
    rows: list[dict] = []

    for n in n_values:
        for label, k in k_values_for_n(n):
            for p in p_values:
                rows.append(
                    {
                        "n": n,
                        "k": k,
                        "caso": label,
                        "p": p,
                        "disponibilidade_analitica": availability_general(n, k, p),
                    }
                )

    return pd.DataFrame(rows)


def plot_availability_vs_p(
    n_values: list[int],
    output_dir: Path,
) -> Path:
    """
    Gráfico 2D: disponibilidade × p para k=1 e k=n (conforme enunciado).
    """
    p_range = np.linspace(0.0, 1.0, 101)
    fig, axes = plt.subplots(1, 2, figsize=(14, 5), sharey=True)

    for ax, k_label, k_fn in zip(
        axes,
        ["k = 1 (consulta)", "k = n (atualização)"],
        [
            lambda n, p: availability_general(n, 1, p),
            lambda n, p: availability_general(n, n, p),
        ],
    ):
        for n in n_values:
            y = [k_fn(n, float(p)) for p in p_range]
            ax.plot(p_range, y, label=f"n = {n}", linewidth=2)

        ax.set_title(k_label)
        ax.set_xlabel("p (probabilidade de disponibilidade por servidor)")
        ax.set_ylabel("Disponibilidade do serviço")
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.grid(True, alpha=0.3)
        ax.legend()

    fig.suptitle("Disponibilidade analítica × p", fontsize=14, fontweight="bold")
    fig.tight_layout()

    path = output_dir / "analitico_disponibilidade_vs_p.png"
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    return path


def plot_k_comparison(
    n: int,
    output_dir: Path,
) -> Path:
    """Compara k=1, ⌈n/2⌉ e k=n para um valor fixo de n."""
    p_range = np.linspace(0.0, 1.0, 101)
    fig, ax = plt.subplots(figsize=(10, 6))

    for label, k in k_values_for_n(n):
        y = [availability_general(n, k, float(p)) for p in p_range]
        ax.plot(p_range, y, label=label, linewidth=2)

    ax.set_title(f"Comparação de k para n = {n}")
    ax.set_xlabel("p")
    ax.set_ylabel("Disponibilidade")
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.grid(True, alpha=0.3)
    ax.legend()
    fig.tight_layout()

    path = output_dir / f"analitico_comparacao_k_n{n}.png"
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    return path


def run_analytical_analysis(output_dir: Path) -> pd.DataFrame:
    """Executa toda a análise analítica e salva tabelas/gráficos."""
    output_dir.mkdir(parents=True, exist_ok=True)

    n_values = [1, 2, 3, 5, 10]
    p_values = [0.5, 0.7, 0.9, 0.95, 0.99]

    table = build_comparison_table(n_values, p_values)
    csv_path = output_dir / "analitico_tabela.csv"
    table.to_csv(csv_path, index=False, float_format="%.6f")

    plot_availability_vs_p(n_values, output_dir)
    for n in [3, 5, 10]:
        plot_k_comparison(n, output_dir)

    print(f"[Analítico] Tabela salva em: {csv_path}")
    return table
