from dataclasses import dataclass
from enum import Enum, auto

class Acao(Enum):
    """Ações possíveis que um agente pode executar no ambiente."""
    MOVER_CIMA = auto()
    MOVER_BAIXO = auto()
    MOVER_ESQUERDA = auto()
    MOVER_DIREITA = auto()
    ASPIRAR = auto()
    NO_OP = auto()

class EstadoCasa(Enum):
    """Estados físicos de cada célula do grid."""
    LIMPO = "LIMPO"
    SUJO = "SUJO"
    OBSTACULO = "OBSTACULO"

@dataclass(frozen=True)
class Percepcao:
    """Percepção sensorial local disponibilizada ao agente."""
    esta_sujo: bool
    bateu: bool
