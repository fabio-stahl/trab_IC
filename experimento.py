"""
Avaliação experimental dos agentes (Projeto 1).

Conforme o enunciado: fixa-se o tamanho do ambiente e executa-se cada agente
para VÁRIAS configurações iniciais possíveis de sujeira, obstáculos e posições
do agente. Registra-se a pontuação de desempenho de cada configuração e a
pontuação MÉDIA GLOBAL. Ao final, geram-se tabelas (terminal + CSV) e gráficos
comparativos entre o Agente Reativo Simples e o Agente Baseado em Modelo.

Medidas de avaliação (do enunciado):
  - Medida 1: +1 ponto para cada quadrado limpo em CADA período.
  - Medida 2: +1 por quadrado limpo e -1 a cada movimento.

Para que a Medida 1 (recompensa por período) seja comparável entre os agentes,
cada episódio roda por um número FIXO de períodos T (tempo de vida do agente).
"""

import os
import csv
import random
import sys
from typing import Callable, Dict, List, Tuple

import matplotlib
matplotlib.use("Agg")  # backend sem interface gráfica (salva PNGs)
import matplotlib.pyplot as plt

from ambiente import Ambiente
from agente_reativo_simples import AgenteReativoSimples
from agente_inteligente import AgenteBaseadoEmModelo
from simulador import Simulador

PASTA_SAIDA = "resultados"

# Fábricas de agentes: recebem uma seed e devolvem um agente novo.
FABRICAS: Dict[str, Callable[[int], object]] = {
    "Reativo Simples": lambda seed: AgenteReativoSimples(seed=seed),
    "Baseado em Modelo": lambda seed: AgenteBaseadoEmModelo(seed=seed),
}


def configurar_terminal() -> None:
    if sys.platform == "win32":
        try:
            sys.stdout.reconfigure(encoding="utf-8")
        except Exception:
            pass


def gerar_configuracoes(
    n_configs: int, largura: int, altura: int, seed_base: int = 1000
) -> List[Dict]:
    """
    Gera n configurações (seed do ambiente + posição inicial do robô).
    Cada configuração define um padrão diferente de sujeira, obstáculos e
    posição inicial; ambos os agentes são avaliados sobre AS MESMAS configurações.
    """
    rng = random.Random(seed_base)
    configs = []
    for i in range(n_configs):
        start = (rng.randrange(largura), rng.randrange(altura))
        configs.append({"seed": i, "start": start})
    return configs


def rodar_episodio(
    fabrica: Callable[[int], object],
    largura: int,
    altura: int,
    taxa_sujeira: float,
    taxa_obstaculo: float,
    config: Dict,
    periodos: int,
) -> Dict:
    """
    Executa UM episódio de tempo de vida fixo (periodos) para um agente sobre
    uma configuração específica de ambiente. Retorna as métricas do episódio.
    """
    ambiente = Ambiente(
        largura=largura,
        altura=altura,
        taxa_sujeira=taxa_sujeira,
        taxa_obstaculo=taxa_obstaculo,
        posicao_inicial=config["start"],
        seed=config["seed"],
    )
    agente = fabrica(config["seed"])
    simulador = Simulador(ambiente=ambiente, agente=agente)

    relatorio = simulador.executar_simulacao(
        total_passos=periodos, parar_ao_limpar_tudo=False, verbose=False
    )

    relatorio["limpou_tudo"] = ambiente.total_casas_sujas() == 0
    relatorio["casas_uteis"] = ambiente.total_casas_uteis()
    return relatorio


def media(valores: List[float]) -> float:
    return sum(valores) / len(valores) if valores else 0.0


def rodar_experimento(
    largura: int = 5,
    altura: int = 5,
    n_configs: int = 50,
    taxa_sujeira: float = 0.20,
    taxa_obstaculo: float = 0.10,
    periodos: int = None,
) -> Dict:
    """
    Roda o experimento completo: n_configs configurações, ambos os agentes,
    tamanho de ambiente FIXO. Devolve resultados por configuração e médias globais.
    """
    if periodos is None:
        periodos = 8 * largura * altura  # tempo de vida generoso

    configs = gerar_configuracoes(n_configs, largura, altura)

    resultados: Dict[str, Dict[str, List]] = {}
    for nome, fabrica in FABRICAS.items():
        linhas = []
        for cfg in configs:
            rel = rodar_episodio(
                fabrica, largura, altura, taxa_sujeira, taxa_obstaculo, cfg, periodos
            )
            linhas.append(rel)
        resultados[nome] = {
            "medida_1": [r["medida_1"] for r in linhas],
            "medida_2": [r["medida_2"] for r in linhas],
            "movimentos": [r["movimentos"] for r in linhas],
            "aspiradas": [r["aspiradas"] for r in linhas],
            "limpou_tudo": [r["limpou_tudo"] for r in linhas],
        }

    return {
        "largura": largura,
        "altura": altura,
        "n_configs": n_configs,
        "taxa_sujeira": taxa_sujeira,
        "taxa_obstaculo": taxa_obstaculo,
        "periodos": periodos,
        "por_agente": resultados,
    }


def imprimir_tabela(exp: Dict) -> None:
    """Imprime no terminal a tabela de médias globais por agente."""
    print("\n" + "=" * 70)
    print("RESUMO DO EXPERIMENTO (médias globais)")
    print(
        f"Ambiente {exp['largura']}x{exp['altura']} | {exp['n_configs']} configurações | "
        f"T={exp['periodos']} períodos | sujeira={exp['taxa_sujeira']:.0%} | "
        f"obstáculos={exp['taxa_obstaculo']:.0%}"
    )
    print("=" * 70)
    cabecalho = f"{'Agente':<20}{'Medida 1':>12}{'Medida 2':>12}{'Movim.':>10}{'Aspir.':>10}{'% Limpou':>10}"
    print(cabecalho)
    print("-" * 70)
    for nome, dados in exp["por_agente"].items():
        pct_limpou = 100.0 * media([1.0 if x else 0.0 for x in dados["limpou_tudo"]])
        print(
            f"{nome:<20}"
            f"{media(dados['medida_1']):>12.1f}"
            f"{media(dados['medida_2']):>12.1f}"
            f"{media(dados['movimentos']):>10.1f}"
            f"{media(dados['aspiradas']):>10.1f}"
            f"{pct_limpou:>9.0f}%"
        )
    print("=" * 70)


def salvar_csv(exp: Dict) -> str:
    """Salva os resultados por configuração e o resumo em arquivos CSV."""
    os.makedirs(PASTA_SAIDA, exist_ok=True)

    # CSV detalhado (uma linha por configuração x agente)
    caminho_det = os.path.join(PASTA_SAIDA, "resultados_por_configuracao.csv")
    with open(caminho_det, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["config", "agente", "medida_1", "medida_2", "movimentos", "aspiradas", "limpou_tudo"])
        for nome, dados in exp["por_agente"].items():
            for i in range(exp["n_configs"]):
                w.writerow([
                    i, nome,
                    dados["medida_1"][i], dados["medida_2"][i],
                    dados["movimentos"][i], dados["aspiradas"][i],
                    dados["limpou_tudo"][i],
                ])

    # CSV resumo (médias globais)
    caminho_res = os.path.join(PASTA_SAIDA, "resumo_medias.csv")
    with open(caminho_res, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["agente", "media_medida_1", "media_medida_2", "media_movimentos", "media_aspiradas", "pct_limpou"])
        for nome, dados in exp["por_agente"].items():
            pct = 100.0 * media([1.0 if x else 0.0 for x in dados["limpou_tudo"]])
            w.writerow([
                nome,
                round(media(dados["medida_1"]), 2),
                round(media(dados["medida_2"]), 2),
                round(media(dados["movimentos"]), 2),
                round(media(dados["aspiradas"]), 2),
                round(pct, 1),
            ])
    return PASTA_SAIDA


# ---------------------------------------------------------------------------
# GRÁFICOS COMPARATIVOS
# ---------------------------------------------------------------------------

COR_REATIVO = "#D9534F"   # vermelho
COR_MODELO = "#4A90D9"    # azul


def _cor(nome: str) -> str:
    return COR_REATIVO if "Reativo" in nome else COR_MODELO


def grafico_medias(exp: Dict) -> str:
    """Barras agrupadas: média das duas medidas por agente."""
    os.makedirs(PASTA_SAIDA, exist_ok=True)
    nomes = list(exp["por_agente"].keys())
    m1 = [media(exp["por_agente"][n]["medida_1"]) for n in nomes]
    m2 = [media(exp["por_agente"][n]["medida_2"]) for n in nomes]

    x = range(len(nomes))
    largura_barra = 0.35
    fig, ax = plt.subplots(figsize=(8, 5))
    b1 = ax.bar([i - largura_barra / 2 for i in x], m1, largura_barra,
                label="Medida 1 (+1/limpo por período)", color="#4A90D9")
    b2 = ax.bar([i + largura_barra / 2 for i in x], m2, largura_barra,
                label="Medida 2 (+limpo -movimento)", color="#D9534F")
    ax.set_xticks(list(x))
    ax.set_xticklabels(nomes)
    ax.set_ylabel("Pontuação média global")
    ax.set_title(f"Desempenho médio por agente ({exp['largura']}x{exp['altura']}, "
                 f"{exp['n_configs']} configurações)")
    ax.legend()
    ax.bar_label(b1, fmt="%.0f", padding=3)
    ax.bar_label(b2, fmt="%.0f", padding=3)
    ax.grid(axis="y", linestyle="--", alpha=0.4)
    fig.tight_layout()
    caminho = os.path.join(PASTA_SAIDA, "grafico_medias.png")
    fig.savefig(caminho, dpi=130)
    plt.close(fig)
    return caminho


def grafico_por_configuracao(exp: Dict) -> str:
    """Linha: Medida 2 por configuração para os dois agentes (mostra variabilidade)."""
    os.makedirs(PASTA_SAIDA, exist_ok=True)
    fig, ax = plt.subplots(figsize=(10, 5))
    for nome, dados in exp["por_agente"].items():
        ax.plot(range(exp["n_configs"]), dados["medida_2"], marker="o",
                markersize=3, linewidth=1.2, label=nome, color=_cor(nome))
    ax.set_xlabel("Configuração do ambiente (nº)")
    ax.set_ylabel("Medida 2 (limpo - movimento)")
    ax.set_title("Medida 2 por configuração — variabilidade entre os agentes")
    ax.legend()
    ax.grid(True, linestyle="--", alpha=0.4)
    fig.tight_layout()
    caminho = os.path.join(PASTA_SAIDA, "grafico_por_configuracao.png")
    fig.savefig(caminho, dpi=130)
    plt.close(fig)
    return caminho


def grafico_esforco(exp: Dict) -> str:
    """Barras: média de movimentos e aspiradas por agente (esforço/eficiência)."""
    os.makedirs(PASTA_SAIDA, exist_ok=True)
    nomes = list(exp["por_agente"].keys())
    movs = [media(exp["por_agente"][n]["movimentos"]) for n in nomes]
    asp = [media(exp["por_agente"][n]["aspiradas"]) for n in nomes]

    x = range(len(nomes))
    largura_barra = 0.35
    fig, ax = plt.subplots(figsize=(8, 5))
    b1 = ax.bar([i - largura_barra / 2 for i in x], movs, largura_barra,
                label="Movimentos", color="#8E44AD")
    b2 = ax.bar([i + largura_barra / 2 for i in x], asp, largura_barra,
                label="Aspiradas", color="#27AE60")
    ax.set_xticks(list(x))
    ax.set_xticklabels(nomes)
    ax.set_ylabel("Média por episódio")
    ax.set_title("Esforço médio: movimentos vs. aspiradas")
    ax.legend()
    ax.bar_label(b1, fmt="%.0f", padding=3)
    ax.bar_label(b2, fmt="%.0f", padding=3)
    ax.grid(axis="y", linestyle="--", alpha=0.4)
    fig.tight_layout()
    caminho = os.path.join(PASTA_SAIDA, "grafico_esforco.png")
    fig.savefig(caminho, dpi=130)
    plt.close(fig)
    return caminho


def experimento_por_tamanho(
    tamanhos: List[int] = (5, 8, 10, 15),
    n_configs: int = 30,
    taxa_sujeira: float = 0.20,
    taxa_obstaculo: float = 0.10,
) -> str:
    """
    Executa o experimento para vários tamanhos de tabuleiro (aproveitando o
    tabuleiro maleável) e plota como as medidas escalam com o tamanho.
    """
    os.makedirs(PASTA_SAIDA, exist_ok=True)
    dados_m1: Dict[str, List[float]] = {n: [] for n in FABRICAS}
    dados_m2: Dict[str, List[float]] = {n: [] for n in FABRICAS}

    for lado in tamanhos:
        exp = rodar_experimento(
            largura=lado, altura=lado, n_configs=n_configs,
            taxa_sujeira=taxa_sujeira, taxa_obstaculo=taxa_obstaculo,
        )
        for nome in FABRICAS:
            dados_m1[nome].append(media(exp["por_agente"][nome]["medida_1"]))
            dados_m2[nome].append(media(exp["por_agente"][nome]["medida_2"]))

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5))
    rotulos = [f"{t}x{t}" for t in tamanhos]
    for nome in FABRICAS:
        ax1.plot(rotulos, dados_m1[nome], marker="o", label=nome, color=_cor(nome))
        ax2.plot(rotulos, dados_m2[nome], marker="o", label=nome, color=_cor(nome))
    ax1.set_title("Medida 1 média vs. tamanho do tabuleiro")
    ax1.set_xlabel("Tamanho do ambiente")
    ax1.set_ylabel("Medida 1 média")
    ax2.set_title("Medida 2 média vs. tamanho do tabuleiro")
    ax2.set_xlabel("Tamanho do ambiente")
    ax2.set_ylabel("Medida 2 média")
    for ax in (ax1, ax2):
        ax.legend()
        ax.grid(True, linestyle="--", alpha=0.4)
    fig.suptitle(f"Escalabilidade dos agentes ({n_configs} configurações por tamanho)")
    fig.tight_layout()
    caminho = os.path.join(PASTA_SAIDA, "grafico_por_tamanho.png")
    fig.savefig(caminho, dpi=130)
    plt.close(fig)
    return caminho


def main() -> None:
    configurar_terminal()
    print("Executando avaliação experimental dos agentes...")

    # 1. Experimento principal (tamanho fixo, muitas configurações)
    exp = rodar_experimento(
        largura=5, altura=5, n_configs=50,
        taxa_sujeira=0.20, taxa_obstaculo=0.10,
    )
    imprimir_tabela(exp)
    salvar_csv(exp)

    # 2. Gráficos comparativos
    g1 = grafico_medias(exp)
    g2 = grafico_por_configuracao(exp)
    g3 = grafico_esforco(exp)

    # 3. Experimento de escalabilidade (tabuleiro maleável)
    g4 = experimento_por_tamanho(tamanhos=[5, 8, 10, 15], n_configs=30)

    print("\nArquivos gerados na pasta 'resultados/':")
    for caminho in (g1, g2, g3, g4):
        print(f"  - {os.path.basename(caminho)}")
    print("  - resultados_por_configuracao.csv")
    print("  - resumo_medias.csv")


if __name__ == "__main__":
    main()
