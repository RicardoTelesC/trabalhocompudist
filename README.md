# Computação Distribuída — Exercícios 1.1 e 1.2

Implementação dos exercícios **1.1** (derivação da fórmula de disponibilidade) e **1.2** (cálculo analítico + simulador estocástico) da disciplina de Computação Distribuída (Prof. Nabor C. Mendonça — UNIFOR).

## Exercício 1.1 — Fórmula de disponibilidade

Serviço replicado em **n** servidores independentes. Cada servidor está disponível com probabilidade **p**. O serviço opera quando **pelo menos k** servidores estão disponíveis.

### Casos extremos

| Caso | Fórmula | Interpretação |
|------|---------|---------------|
| **k = 1** | `A(n,1,p) = 1 − (1−p)ⁿ` | Consulta — basta um servidor |
| **k = n** | `A(n,n,p) = pⁿ` | Atualização — todos devem estar ativos |

### Fórmula geral

```
A(n,k,p) = Σ(i=k..n) C(n,i) · pⁱ · (1−p)ⁿ⁻ⁱ
```

A derivação completa está em [`exercicio_1_1.md`](exercicio_1_1.md).

## Exercício 1.2 — Análise e simulação

### 1. Cálculo analítico

- Implementação da fórmula em Python (`src/availability.py`)
- Tabela comparando **k = 1**, **k = ⌈n/2⌉** e **k = n** para diversos valores de **n** e **p**
- Gráficos 2D de disponibilidade × **p**

### 2. Simulador estocástico

- Simulação Monte Carlo com N rodadas (padrão: 100.000)
- Em cada rodada, cada servidor fica disponível com probabilidade **p**
- Compara frequência experimental com valor analítico
- Gráficos de convergência e teoria vs. prática

## Requisitos

- Python 3.10+
- Dependências listadas em `requirements.txt`

## Como executar

```bash
# 1. Clone o repositório
git clone <url-do-repositorio>
cd compudist

# 2. Crie e ative um ambiente virtual (recomendado)
python -m venv .venv

# Windows
.venv\Scripts\activate

# Linux/macOS
source .venv/bin/activate

# 3. Instale as dependências
pip install -r requirements.txt

# 4. Execute
python main.py
```

### Opções

```bash
# Alterar número de rodadas da simulação
python main.py --rounds 500000

# Alterar diretório de saída
python main.py --output resultados
```

## Saídas geradas

Após a execução, o diretório `output/` conterá:

| Arquivo | Descrição |
|---------|-----------|
| `analitico_tabela.csv` | Disponibilidade analítica para vários n, k, p |
| `analitico_disponibilidade_vs_p.png` | Gráfico k=1 e k=n × p |
| `analitico_comparacao_k_n*.png` | Comparação entre valores de k |
| `simulacao_tabela.csv` | Analítico vs. experimental lado a lado |
| `simulacao_analitico_vs_experimental.png` | Dispersão teoria × simulação |
| `simulacao_convergencia_*.png` | Convergência com número de rodadas |

## Estrutura do projeto

```
compudist/
├── README.md
├── exercicio_1_1.md      # Derivação matemática (1.1)
├── requirements.txt
├── main.py               # Ponto de entrada
├── src/
│   ├── availability.py   # Fórmulas analíticas
│   ├── analytical.py     # Análise e gráficos analíticos
│   └── simulator.py      # Simulador estocástico
└── output/               # Gerado ao executar (ignorado no git)
```

## Referência

Mendonça, N. C. *Computação Distribuída: Exercícios I*. Centro de Ciências Tecnológicos, Universidade de Fortaleza.
