#!/usr/bin/env python3
"""
Computação Distribuída — Exercícios 1.1 e 1.2

Executa análise analítica e simulação estocástica de disponibilidade
de serviço replicado em múltiplos servidores.
"""

from __future__ import annotations

import argparse
from pathlib import Path

from src.analytical import run_analytical_analysis
from src.availability import availability_general, availability_read, availability_write
from src.simulator import run_simulation


def validate_formulas() -> None:
    """Verifica casos extremos k=1 e k=n contra fórmulas fechadas."""
    test_cases = [(3, 0.9), (5, 0.95), (10, 0.99)]
    print("\n=== Validação das fórmulas (Exercício 1.1) ===")
    for n, p in test_cases:
        general_k1 = availability_general(n, 1, p)
        closed_k1 = availability_read(n, p)
        general_kn = availability_general(n, n, p)
        closed_kn = availability_write(n, p)
        print(
            f"n={n}, p={p}: "
            f"k=1 -> geral={general_k1:.6f}, fechada={closed_k1:.6f} | "
            f"k=n -> geral={general_kn:.6f}, fechada={closed_kn:.6f}"
        )


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Exercícios 1.1 e 1.2 — Disponibilidade de serviço replicado"
    )
    parser.add_argument(
        "--rounds",
        type=int,
        default=100_000,
        help="Número de rodadas da simulação (padrão: 100000)",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("output"),
        help="Diretório de saída para tabelas e gráficos",
    )
    args = parser.parse_args()

    print("Computação Distribuída — Exercícios 1.1 e 1.2")
    print("=" * 50)

    validate_formulas()

    print("\n=== Análise analítica (Exercício 1.2 — parte 1) ===")
    analytical_table = run_analytical_analysis(args.output)
    print(analytical_table.head(10).to_string(index=False))

    print(f"\n=== Simulação estocástica (Exercício 1.2 — parte 2, {args.rounds} rodadas) ===")
    simulation_table = run_simulation(args.output, rounds=args.rounds)
    print(simulation_table.head(10).to_string(index=False))

    print(f"\nResultados salvos em: {args.output.resolve()}")


if __name__ == "__main__":
    main()
