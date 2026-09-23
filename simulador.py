from typing import Optional, Dict, Any
from tipos import Acao
from ambiente import Ambiente
from agente_base import Agente
from metricas import AvaliadorDesempenho

class Simulador:
    """Orquestra o ciclo de vida da simulação conectando Ambiente, Agente e Métricas."""

    def __init__(self, ambiente: Ambiente, agente: Agente, avaliador: Optional[AvaliadorDesempenho] = None) -> None:
        self.ambiente = ambiente
        self.agente = agente
        self.avaliador = avaliador if avaliador is not None else AvaliadorDesempenho()
        self.passo_atual: int = 0

    def executar_passo(self, verbose: bool = False) -> Dict[str, Any]:
        """Executa um único ciclo: Percepção -> Decisão -> Atuação -> Avaliação."""
        self.passo_atual += 1

        # 1. Percepção sensorial local
        percepcao = self.ambiente.obter_percepcao()

        # 2. Tomada de decisão do agente
        acao = self.agente.agir(percepcao)

        # 3. Execução física no ambiente
        self.ambiente.executar_acao(acao)

        # 4. Avaliação das métricas de desempenho no período
        casas_limpas = self.ambiente.total_casas_limpas()
        self.avaliador.registrar_periodo(casas_limpas, acao)

        if verbose:
            self._imprimir_passo(acao, percepcao, casas_limpas)

        return {
            "passo": self.passo_atual,
            "acao": acao.name,
            "casas_limpas": casas_limpas,
            "casas_sujas": self.ambiente.total_casas_sujas(),
        }

    def executar_simulacao(self, total_passos: int = 50, verbose: bool = False) -> Dict[str, Any]:
        """Executa a simulação completa pelo número estipulado de passos de tempo."""
        if verbose:
            print("=" * 45)
            print(f"ESTADO INICIAL (Robô em {self.ambiente.posicao_agente}):")
            print(self.ambiente.renderizar())
            print(f"Total Sujas: {self.ambiente.total_casas_sujas()}/25 (20%)")
            print("=" * 45)

        for _ in range(total_passos):
            self.executar_passo(verbose=verbose)

        relatorio = self.avaliador.obter_relatorio()
        relatorio["passos_totais"] = self.passo_atual
        relatorio["sujeiras_restantes"] = self.ambiente.total_casas_sujas()
        return relatorio

    def _imprimir_passo(self, acao: Acao, percepcao: Any, casas_limpas: int) -> None:
        """Exibe no terminal o estado após cada passo executado."""
        print(f"\n--- Passo {self.passo_atual:02d} | Ação: {acao.name} ---")
        print(f"Percepção: [Sujo: {percepcao.esta_sujo}, Bateu: {percepcao.bateu}]")
        print(f"Posição do Robô: {self.ambiente.posicao_agente} | Casas Limpas: {casas_limpas}/25")
        print(self.ambiente.renderizar())
