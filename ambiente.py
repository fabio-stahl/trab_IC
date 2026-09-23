import random
from typing import Dict, Tuple, Optional
from tipos import Acao, EstadoCasa, Percepcao

class Ambiente:
    """
    Ambiente físico 5x5 determinístico e parcialmente observável em plano cartesiano.
    A origem (0, 0) localiza-se no canto inferior esquerdo (eixo X horizontal, eixo Y vertical).
    """

    # Deslocamentos cartesianos: (dx, dy)
    DESLOCAMENTOS = {
        Acao.MOVER_CIMA: (0, 1),
        Acao.MOVER_BAIXO: (0, -1),
        Acao.MOVER_ESQUERDA: (-1, 0),
        Acao.MOVER_DIREITA: (1, 0),
    }

    def __init__(
        self,
        largura: int = 5,
        altura: int = 5,
        taxa_sujeira: float = 0.20,
        posicao_inicial: Optional[Tuple[int, int]] = (0, 0),
        seed: Optional[int] = None,
        linhas: Optional[int] = None,
        colunas: Optional[int] = None
    ) -> None:
        self.largura = colunas if colunas is not None else largura
        self.altura = linhas if linhas is not None else altura
        self.taxa_sujeira = taxa_sujeira
        self._rng = random.Random(seed)

        self.grid: Dict[Tuple[int, int], EstadoCasa] = {}
        self.posicao_agente: Tuple[int, int] = (0, 0)
        self.bateu: bool = False

        self.reiniciar(posicao_inicial)

    def reiniciar(self, posicao_inicial: Optional[Tuple[int, int]] = (0, 0)) -> None:
        """Reinicia o grid com 20% de sujeira e redefine a posição inicial do robô."""
        self._criar_grid_limpo()
        self._distribuir_sujeiras()
        self._definir_posicao_agente(posicao_inicial)
        self.bateu = False

    def _criar_grid_limpo(self) -> None:
        """Inicializa todas as coordenadas cartesianas (x, y) como limpas."""
        self.grid = {
            (x, y): EstadoCasa.LIMPO
            for x in range(self.largura)
            for y in range(self.altura)
        }

    def _distribuir_sujeiras(self) -> None:
        """Sorteia exatamente 20% das coordenadas para receber sujeira."""
        total_casas = self.largura * self.altura
        total_sujas = int(total_casas * self.taxa_sujeira)

        todas_posicoes = list(self.grid.keys())
        posicoes_sujas = self._rng.sample(todas_posicoes, total_sujas)

        for pos in posicoes_sujas:
            self.grid[pos] = EstadoCasa.SUJO

    def _definir_posicao_agente(self, posicao_inicial: Optional[Tuple[int, int]]) -> None:
        """Define coordenada (x, y) do agente (padrão (0, 0) no canto inferior esquerdo)."""
        if posicao_inicial is not None:
            self.posicao_agente = posicao_inicial
        else:
            self.posicao_agente = (0, 0)

    def obter_percepcao(self) -> Percepcao:
        """Sensor local: verifica se o ponto atual (x, y) está sujo e se bateu."""
        esta_sujo = (self.grid[self.posicao_agente] == EstadoCasa.SUJO)
        return Percepcao(esta_sujo=esta_sujo, bateu=self.bateu)

    def executar_acao(self, acao: Acao) -> None:
        """Aplica a ação física no plano cartesiano e atualiza sensor de colisão."""
        if acao == Acao.ASPIRAR:
            self.grid[self.posicao_agente] = EstadoCasa.LIMPO
            self.bateu = False
        elif acao in self.DESLOCAMENTOS:
            dx, dy = self.DESLOCAMENTOS[acao]
            x, y = self.posicao_agente
            nx, ny = x + dx, y + dy

            # Valida limites no plano cartesiano
            if 0 <= nx < self.largura and 0 <= ny < self.altura:
                self.posicao_agente = (nx, ny)
                self.bateu = False
            else:
                self.bateu = True
        else:
            self.bateu = False

    def total_casas_limpas(self) -> int:
        """Retorna quantidade de coordenadas limpas."""
        return sum(1 for estado in self.grid.values() if estado == EstadoCasa.LIMPO)

    def total_casas_sujas(self) -> int:
        """Retorna quantidade de coordenadas sujas."""
        return sum(1 for estado in self.grid.values() if estado == EstadoCasa.SUJO)

    def renderizar(self) -> str:
        """
        Gera representação visual cartesiana:
        O topo é y máximo e a base é y=0. Da esquerda (x=0) para a direita (x máximo).
        """
        linhas_str = []
        for y in range(self.altura - 1, -1, -1):
            tokens = [f"y={y} |"]
            for x in range(self.largura):
                is_robo = (x, y) == self.posicao_agente
                is_sujo = self.grid[(x, y)] == EstadoCasa.SUJO

                if is_robo and is_sujo:
                    tokens.append("[R*]")
                elif is_robo:
                    tokens.append("[ R]")
                elif is_sujo:
                    tokens.append("[ *]")
                else:
                    tokens.append("[ .]")
            linhas_str.append(" ".join(tokens))

        # Adiciona legenda dos eixos X
        eixo_x = "     + " + " ".join([f"x={x}" for x in range(self.largura)])
        linhas_str.append(eixo_x)
        return "\n".join(linhas_str)