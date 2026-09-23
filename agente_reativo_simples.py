import random
from typing import Optional, List
from tipos import Acao, Percepcao
from agente_base import Agente

class AgenteReativoSimples(Agente):
    """
    Agente Reativo Simples: decide ações puramente com base na percepção imediata,
    orientado por regras condição-ação e sem manter histórico de estados (sem memória).
    """

    DIRECOES_MOVIMENTO: List[Acao] = [
        Acao.MOVER_CIMA,
        Acao.MOVER_BAIXO,
        Acao.MOVER_ESQUERDA,
        Acao.MOVER_DIREITA,
    ]

    def __init__(self, seed: Optional[int] = None) -> None:
        self._rng = random.Random(seed)
        self.direcao_atual: Acao = self._escolher_direcao_aleatoria()

    def agir(self, percepcao: Percepcao) -> Acao:
        """Aplica regras condição-ação com base na percepção sensorial atual."""
        # Regra 1: Se a célula atual estiver suja, aspira imediatamente
        if percepcao.esta_sujo:
            return Acao.ASPIRAR

        # Regra 2: Se colidiu com uma parede, altera a direção para desobstrução
        if percepcao.bateu:
            self.direcao_atual = self._mudar_direcao_apos_colisao()
            return self.direcao_atual

        # Regra 3: Se limpo e desobstruído, avança na direção atual (com chance de virar)
        if self._rng.random() < 0.25:
            self.direcao_atual = self._escolher_direcao_aleatoria()

        return self.direcao_atual

    def _escolher_direcao_aleatoria(self) -> Acao:
        """Sorteia uma direção de movimento uniforme."""
        return self._rng.choice(self.DIRECOES_MOVIMENTO)

    def _mudar_direcao_apos_colisao(self) -> Acao:
        """Reflexo de colisão: escolhe uma nova direção diferente da que colidiu."""
        outras_direcoes = [d for d in self.DIRECOES_MOVIMENTO if d != self.direcao_atual]
        return self._rng.choice(outras_direcoes)

    def reiniciar(self) -> None:
        """Redefine a direção inicial do agente para novo episódio."""
        self.direcao_atual = self._escolher_direcao_aleatoria()
