<<<<<<< HEAD
import random
from collections import deque
from typing import Optional, List, Dict, Tuple, Set
from tipos import Acao, Percepcao
from agente_base import Agente

Pos = Tuple[int, int]


class AgenteBaseadoEmModelo(Agente):

    DESLOCAMENTOS: Dict[Acao, Pos] = {
        Acao.MOVER_CIMA: (0, 1),
        Acao.MOVER_BAIXO: (0, -1),
        Acao.MOVER_ESQUERDA: (-1, 0),
        Acao.MOVER_DIREITA: (1, 0),
    }

    ORDEM_VIZINHOS: List[Acao] = [
        Acao.MOVER_DIREITA,
        Acao.MOVER_CIMA,
        Acao.MOVER_ESQUERDA,
        Acao.MOVER_BAIXO,
    ]

    def __init__(self) -> None:
        self._inicializar_estado()

    
    def _inicializar_estado(self) -> None:
        self.pos: Pos = (0, 0)
        self.visitadas: Set[Pos] = {(0, 0)}
        self.paredes: Set[Pos] = set()
        self.ultima_acao: Optional[Acao] = None
        self.plano: List[Acao] = []

    def _reset_memoria(self) -> None:
        self.pos: Pos = (0, 0)                 
        self.limpas: Set[Pos] = {(0, 0)}       
        self.paredes: Set[Pos] = set()         
        self.ultima_acao: Optional[Acao] = None
        self.plano: List[Acao] = []            

    
    def agir(self, percepcao: Percepcao) -> Acao:
        self._atualizar_estado(percepcao)

        if percepcao.esta_sujo:
            self.ultima_acao = Acao.ASPIRAR
            return Acao.ASPIRAR

        self.limpas.add(self.pos)

        if not self.plano:
            self.plano = self._planejar_ate_fronteira()

        if not self.plano:
            self.ultima_acao = None
            return getattr(Acao, "PARAR", Acao.ASPIRAR)

        acao = self.plano.pop(0)
        self.ultima_acao = acao
        return acao

    def _atualizar_estado(self, percepcao: Percepcao) -> None:
        """UPDATE-STATE: integra a última ação e a percepção atual ao modelo."""
        if self.ultima_acao in self.DESLOCAMENTOS:
            dx, dy = self.DESLOCAMENTOS[self.ultima_acao]
            destino = (self.pos[0] + dx, self.pos[1] + dy)

            if percepcao.bateu:
                # Não saiu do lugar: o destino é parede
                self.paredes.add(destino)
                self.plano = []  # o plano antigo pode passar pela parede
            else:
                self.pos = destino
                self.visitadas.add(self.pos)

    def agir(self,percepcao:Percepcao) -> Acao:
        self._atualizar_estado(percepcao)

        if percepcao.esta_sujo:
            self.ultima_acao = Acao.ASPIRAR
            return Acao.ASPIRAR

        if not self.plano:
            self.ultima_acao = Acao.NO_OP
            return Acao.NO_OP

        acao = self.plano.pop(0)
        self.ultima_acao = acao
        return acao
=======
"""
Módulo compatível com o nome de arquivo com espaço criado anteriormente.
Redireciona para o módulo padrão Python 'agente_inteligente.py'.
"""
from agente_inteligente import (
    AgenteBaseadoEmModelo,
    AgenteInteligente,
    RoboBaseadoEmModelo,
    RoboInteligente,
)

__all__ = [
    "AgenteBaseadoEmModelo",
    "AgenteInteligente",
    "RoboBaseadoEmModelo",
    "RoboInteligente",
]
>>>>>>> bf4e342e6d738fa20e4987f27465a3495d4030f0
