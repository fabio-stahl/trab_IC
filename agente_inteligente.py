from collections import deque
from typing import Optional, List, Dict, Tuple, Set
from tipos import Acao, Percepcao
from agente_base import Agente

Pos = Tuple[int, int]

class AgenteBaseadoEmModelo(Agente):
    """
    Agente Reativo Baseado em Modelos (Inteligente):
    Mantém um estado interno (modelo de mundo) a respeito do ambiente cartesiano,
    rastreando sua posição estimada, células visitadas, paredes/obstáculos detectados
    e células limpas.
    
    A tomada de decisão é orientada por regras condição-ação e planejamento
    por busca em largura (BFS) até a fronteira desconhecida mais próxima.
    Quando todas as células acessíveis forem visitadas e limpas, adota NO_OP
    para maximizar a pontuação e economizar movimentos (racionalidade).
    """

    # Deslocamentos cartesianos correspondentes a cada ação: (dx, dy)
    DESLOCAMENTOS: Dict[Acao, Pos] = {
        Acao.MOVER_CIMA: (0, 1),
        Acao.MOVER_BAIXO: (0, -1),
        Acao.MOVER_ESQUERDA: (-1, 0),
        Acao.MOVER_DIREITA: (1, 0),
    }

    # Ordem sistemática de exploração de vizinhos
    ORDEM_VIZINHOS: List[Acao] = [
        Acao.MOVER_DIREITA,
        Acao.MOVER_CIMA,
        Acao.MOVER_ESQUERDA,
        Acao.MOVER_BAIXO,
    ]

    def __init__(self, seed: Optional[int] = None) -> None:
        """Inicializa o agente e seu modelo de mundo interno."""
        self.reiniciar()

    def reiniciar(self) -> None:
        """Reinicia o estado interno do agente para um novo episódio de simulação."""
        self.pos: Pos = (0, 0)
        self.visitadas: Set[Pos] = {(0, 0)}
        self.paredes: Set[Pos] = set()
        self.limpas: Set[Pos] = set()
        self.ultima_acao: Optional[Acao] = None
        self.plano: List[Acao] = []

    def _inicializar_estado(self) -> None:
        """Alias para reiniciar o estado."""
        self.reiniciar()

    def _reset_memoria(self) -> None:
        """Alias para reiniciar a memória interna."""
        self.reiniciar()

    def _atualizar_estado(self, percepcao: Percepcao) -> None:
        """
        UPDATE-STATE: Integra a última ação executada e a percepção sensorial
        atual ao modelo interno de mundo do agente.
        """
        if self.ultima_acao in self.DESLOCAMENTOS:
            dx, dy = self.DESLOCAMENTOS[self.ultima_acao]
            destino: Pos = (self.pos[0] + dx, self.pos[1] + dy)

            if percepcao.bateu:
                # O movimento colidiu: a coordenada de destino é identificada como parede
                self.paredes.add(destino)
                # Invalida o plano restante, pois o caminho pretendido foi obstruído
                self.plano.clear()
            else:
                # O movimento teve sucesso: atualiza a posição e marca como visitada
                self.pos = destino
                self.visitadas.add(self.pos)
        elif self.ultima_acao == Acao.ASPIRAR:
            # Conclusão da ação de aspirar a célula atual
            self.limpas.add(self.pos)

        # Se a percepção sensorial confirma que a célula atual não está suja
        if not percepcao.esta_sujo:
            self.limpas.add(self.pos)

    def _planejar_ate_fronteira(self) -> List[Acao]:
        """
        Busca em Largura (BFS): Encontra a sequência mínima de ações para alcançar
        a célula desconhecida (fronteira) mais próxima, trafegando estritamente
        por células já conhecidas e transitáveis (self.visitadas).
        """
        fila: deque[Tuple[Pos, List[Acao]]] = deque([(self.pos, [])])
        visitados_busca: Set[Pos] = {self.pos}

        while fila:
            pos_atual, caminho = fila.popleft()

            for acao in self.ORDEM_VIZINHOS:
                dx, dy = self.DESLOCAMENTOS[acao]
                vizinho: Pos = (pos_atual[0] + dx, pos_atual[1] + dy)

                if vizinho in self.paredes:
                    continue

                if vizinho not in self.visitadas:
                    # Encontrou o passo que leva à célula não visitada mais próxima
                    return caminho + [acao]

                if vizinho not in visitados_busca:
                    visitados_busca.add(vizinho)
                    fila.append((vizinho, caminho + [acao]))

        # Nenhuma fronteira acessível restante (ambiente totalmente explorado)
        return []

    def agir(self, percepcao: Percepcao) -> Acao:
        """
        Ciclo de deliberação:
        1. Atualiza o modelo de mundo (UPDATE-STATE)
        2. Aplica regras condição-ação e execução/geração de planos
        """
        self._atualizar_estado(percepcao)

        # Regra Condição-Ação 1: Se a célula atual estiver suja, aspira imediatamente
        if percepcao.esta_sujo:
            self.ultima_acao = Acao.ASPIRAR
            return Acao.ASPIRAR

        # Regra Condição-Ação 2: Se não houver plano ativo, gera plano até a fronteira
        if not self.plano:
            self.plano = self._planejar_ate_fronteira()

        # Regra Condição-Ação 3: Se não há fronteira acessível, todas as casas
        # foram visitadas e limpas -> Permanece em NO_OP para não sofrer penalidade de movimento
        if not self.plano:
            self.ultima_acao = Acao.NO_OP
            return Acao.NO_OP

        # Regra Condição-Ação 4: Extrai e executa o próximo passo do plano
        acao = self.plano.pop(0)
        self.ultima_acao = acao
        return acao

# Aliases para compatibilidade e flexibilidade
AgenteInteligente = AgenteBaseadoEmModelo
RoboInteligente = AgenteBaseadoEmModelo
RoboBaseadoEmModelo = AgenteBaseadoEmModelo
