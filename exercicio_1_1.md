# Exercício 1.1 — Disponibilidade de Serviço Replicado

## Modelo

Considere um serviço replicado em **n** servidores independentes. Cada servidor está
disponível em um dado instante com probabilidade **p** (e indisponível com probabilidade
**1 − p**). O serviço permanece operacional quando **pelo menos k** servidores estão
disponíveis simultaneamente, com **0 < k ≤ n**.

O número de servidores disponíveis segue uma **distribuição binomial** Bin(n, p).

## Casos extremos

### k = 1 (operação de consulta — tolerância máxima a falhas)

Basta **um** servidor estar disponível. A indisponibilidade ocorre somente quando
**todos** os n servidores falham:

\[
A(n, 1, p) = 1 - (1 - p)^n
\]

### k = n (operação de atualização — todos devem estar disponíveis)

Todos os **n** servidores precisam estar disponíveis:

\[
A(n, n, p) = p^n
\]

## Fórmula geral

Para **k** arbitrário, a disponibilidade é a probabilidade de haver **k ou mais**
sucessos em n tentativas independentes:

\[
A(n, k, p) = \sum_{i=k}^{n} \binom{n}{i} \, p^i \, (1-p)^{n-i}
\]

Equivalentemente, usando a função de distribuição acumulada da binomial:

\[
A(n, k, p) = 1 - \sum_{i=0}^{k-1} \binom{n}{i} \, p^i \, (1-p)^{n-i}
\]

## Interpretação

| Parâmetro | Significado |
|-----------|-------------|
| **n** | Número total de servidores replicados |
| **k** | Quorum mínimo para o serviço operar de forma consistente |
| **p** | Probabilidade de cada servidor individual estar disponível |

- **k = 1**: máxima tolerância a falhas (leitura com réplicas).
- **k = n**: consistência forte (escrita em todos os nós).
- **k = ⌈n/2⌉ + 1**: quorum majoritário em sistemas replicados.
