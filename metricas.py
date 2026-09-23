from tipos import Acao

class AvaliadorDesempenho:
    """Calcula e armazena as duas medidas de avaliação estabelecidas no projeto."""

    ACOES_MOVIMENTO = {
        Acao.MOVER_CIMA,
        Acao.MOVER_BAIXO,
        Acao.MOVER_ESQUERDA,
        Acao.MOVER_DIREITA,
    }

    def __init__(self) -> None:
        self.pontuacao_medida_1: int = 0
        self.pontuacao_medida_2: int = 0
        self.total_movimentos: int = 0
        self.total_aspiradas: int = 0

    def registrar_periodo(self, total_casas_limpas: int, acao_executada: Acao) -> None:
        """Atualiza as pontuações a cada período de tempo 't'."""
        # Medida 1: +1 ponto para cada quadrado limpo em cada período
        self.pontuacao_medida_1 += total_casas_limpas

        # Medida 2: +1 ponto para cada quadrado limpo e penaliza -1 por movimento
        custo_movimento = 1 if acao_executada in self.ACOES_MOVIMENTO else 0
        self.pontuacao_medida_2 += total_casas_limpas - custo_movimento

        if custo_movimento > 0:
            self.total_movimentos += 1
        elif acao_executada == Acao.ASPIRAR:
            self.total_aspiradas += 1

    def reiniciar(self) -> None:
        """Zera as métricas para um novo experimento."""
        self.pontuacao_medida_1 = 0
        self.pontuacao_medida_2 = 0
        self.total_movimentos = 0
        self.total_aspiradas = 0

    def obter_relatorio(self) -> dict:
        """Retorna resumo quantitativo de desempenho."""
        return {
            "medida_1": self.pontuacao_medida_1,
            "medida_2": self.pontuacao_medida_2,
            "movimentos": self.total_movimentos,
            "aspiradas": self.total_aspiradas,
        }
