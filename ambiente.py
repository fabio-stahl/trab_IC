import random
from collections import deque
from typing import Dict, Tuple, Optional, List, Set
from tipos import Acao, EstadoCasa, Percepcao

Pos = Tuple[int, int]


class Ambiente:
    """
    Ambiente físico determinístico e parcialmente observável em plano cartesiano.
    A origem (0, 0) localiza-se no canto inferior esquerdo (eixo X horizontal, eixo Y vertical).

    O ambiente possui tamanho configurável (largura x altura), sujeira distribuída
    aleatoriamente e obstáculos internos (paredes) que o agente não conhece de
    antemão e só descobre localmente por meio do sensor de colisão ("bateu").
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
        taxa_obstaculo: float = 0.0,
        posicao_inicial: Optional[Tuple[int, int]] = (0, 0),
        seed: Optional[int] = None,
        linhas: Optional[int] = None,
        colunas: Optional[int] = None
    ) -> None:
        self.largura = colunas if colunas is not None else largura
        self.altura = linhas if linhas is not None else altura
        self.taxa_sujeira = taxa_sujeira
        self.taxa_obstaculo = taxa_obstaculo
        self._rng = random.Random(seed)

        self.grid: Dict[Pos, EstadoCasa] = {}
        self.posicao_agente: Pos = (0, 0)
        self.bateu: bool = False

        self.reiniciar(posicao_inicial)

    def reiniciar(self, posicao_inicial: Optional[Tuple[int, int]] = (0, 0)) -> None:
        """Reinicia o grid: cria obstáculos, distribui sujeira e posiciona o robô."""
        self._criar_grid_limpo()
        self._definir_posicao_agente(posicao_inicial)
        self._distribuir_obstaculos()
        self._distribuir_sujeiras()
        self.bateu = False

    def _criar_grid_limpo(self) -> None:
        """Inicializa todas as coordenadas cartesianas (x, y) como limpas."""
        self.grid = {
            (x, y): EstadoCasa.LIMPO
            for x in range(self.largura)
            for y in range(self.altura)
        }

    def _definir_posicao_agente(self, posicao_inicial: Optional[Tuple[int, int]]) -> None:
        """Define coordenada (x, y) do agente (padrão (0, 0) no canto inferior esquerdo)."""
        if posicao_inicial is not None:
            self.posicao_agente = posicao_inicial
        else:
            self.posicao_agente = (0, 0)

    def _distribuir_obstaculos(self) -> None:
        """
        Sorteia coordenadas para receber obstáculos internos.

        A célula inicial do agente nunca recebe obstáculo. Um obstáculo só é
        efetivamente colocado se NÃO isolar nenhuma célula livre (o tabuleiro
        permanece totalmente conectado a partir da posição inicial). Isso evita
        ambientes degenerados em que o robô fica "ilhado".
        """
        if self.taxa_obstaculo <= 0:
            return

        total_casas = self.largura * self.altura
        alvo_obstaculos = int(total_casas * self.taxa_obstaculo)

        candidatas = [p for p in self.grid.keys() if p != self.posicao_agente]
        self._rng.shuffle(candidatas)

        colocados = 0
        for pos in candidatas:
            if colocados >= alvo_obstaculos:
                break
            self.grid[pos] = EstadoCasa.OBSTACULO
            livres_restantes = total_casas - (colocados + 1)
            # Mantém o obstáculo apenas se todas as células livres continuam acessíveis
            if len(self._celulas_alcancaveis()) == livres_restantes:
                colocados += 1
            else:
                self.grid[pos] = EstadoCasa.LIMPO  # desfaz: isolaria células

    def _celulas_alcancaveis(self) -> Set[Pos]:
        """
        BFS a partir da posição inicial do agente sobre células livres
        (não obstáculo). Retorna o conjunto de coordenadas alcançáveis.
        """
        alcancaveis: Set[Pos] = set()
        fila: deque[Pos] = deque([self.posicao_agente])
        alcancaveis.add(self.posicao_agente)

        while fila:
            x, y = fila.popleft()
            for dx, dy in self.DESLOCAMENTOS.values():
                viz = (x + dx, y + dy)
                if (0 <= viz[0] < self.largura and 0 <= viz[1] < self.altura
                        and viz not in alcancaveis
                        and self.grid.get(viz) != EstadoCasa.OBSTACULO):
                    alcancaveis.add(viz)
                    fila.append(viz)
        return alcancaveis

    def _distribuir_sujeiras(self) -> None:
        """
        Sorteia células para receber sujeira. A sujeira é colocada apenas em
        células alcançáveis a partir da posição inicial (garante episódios
        solucionáveis), exceto a célula onde o robô inicia.
        """
        alcancaveis = self._celulas_alcancaveis()
        candidatas = [p for p in alcancaveis if p != self.posicao_agente]

        if not candidatas:
            return

        total_sujas = round(len(candidatas) * self.taxa_sujeira)
        # Garante ao menos uma sujeira quando a taxa é positiva e há espaço
        if self.taxa_sujeira > 0 and total_sujas == 0:
            total_sujas = 1
        total_sujas = max(0, min(total_sujas, len(candidatas)))
        posicoes_sujas = self._rng.sample(candidatas, total_sujas)

        for pos in posicoes_sujas:
            self.grid[pos] = EstadoCasa.SUJO

    def obter_percepcao(self) -> Percepcao:
        """Sensor local: verifica se o ponto atual (x, y) está sujo e se bateu."""
        esta_sujo = (self.grid[self.posicao_agente] == EstadoCasa.SUJO)
        return Percepcao(esta_sujo=esta_sujo, bateu=self.bateu)

    def executar_acao(self, acao: Acao) -> None:
        """Aplica a ação física no plano cartesiano e atualiza sensor de colisão."""
        if acao == Acao.ASPIRAR:
            if self.grid[self.posicao_agente] == EstadoCasa.SUJO:
                self.grid[self.posicao_agente] = EstadoCasa.LIMPO
            self.bateu = False
        elif acao in self.DESLOCAMENTOS:
            dx, dy = self.DESLOCAMENTOS[acao]
            x, y = self.posicao_agente
            nx, ny = x + dx, y + dy
            destino = (nx, ny)

            # Bloqueia por limites do ambiente OU por obstáculo interno
            dentro_limites = 0 <= nx < self.largura and 0 <= ny < self.altura
            eh_obstaculo = self.grid.get(destino) == EstadoCasa.OBSTACULO

            if dentro_limites and not eh_obstaculo:
                self.posicao_agente = destino
                self.bateu = False
            else:
                self.bateu = True
        else:
            self.bateu = False

    def total_casas_limpas(self) -> int:
        """Retorna quantidade de coordenadas limpas (não conta obstáculos)."""
        return sum(1 for estado in self.grid.values() if estado == EstadoCasa.LIMPO)

    def total_casas_sujas(self) -> int:
        """Retorna quantidade de coordenadas sujas."""
        return sum(1 for estado in self.grid.values() if estado == EstadoCasa.SUJO)

    def total_obstaculos(self) -> int:
        """Retorna quantidade de coordenadas com obstáculo."""
        return sum(1 for estado in self.grid.values() if estado == EstadoCasa.OBSTACULO)

    def total_casas_uteis(self) -> int:
        """Total de células que podem ser limpas (não obstáculo)."""
        return self.largura * self.altura - self.total_obstaculos()

    def renderizar(self) -> str:
        """
        Gera representação visual cartesiana:
        O topo é y máximo e a base é y=0. Da esquerda (x=0) para a direita (x máximo).
        Legenda: [ R] robô, [R*] robô sobre sujeira, [ *] sujeira, [##] obstáculo, [ .] limpo.
        """
        linhas_str = []
        for y in range(self.altura - 1, -1, -1):
            tokens = [f"y={y:>2} |"]
            for x in range(self.largura):
                estado = self.grid[(x, y)]
                is_robo = (x, y) == self.posicao_agente

                if estado == EstadoCasa.OBSTACULO:
                    tokens.append("[##]")
                elif is_robo and estado == EstadoCasa.SUJO:
                    tokens.append("[R*]")
                elif is_robo:
                    tokens.append("[ R]")
                elif estado == EstadoCasa.SUJO:
                    tokens.append("[ *]")
                else:
                    tokens.append("[ .]")
            linhas_str.append(" ".join(tokens))

        eixo_x = "      + " + " ".join([f"x={x}" for x in range(self.largura)])
        linhas_str.append(eixo_x)
        return "\n".join(linhas_str)
