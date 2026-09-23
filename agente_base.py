from abc import ABC, abstractmethod
from tipos import Acao, Percepcao

class Agente(ABC):
    """Interface base abstrata para agentes inteligentes (Princípio OCP/DIP)."""

    @abstractmethod
    def agir(self, percepcao: Percepcao) -> Acao:
        """Recebe a percepção sensorial local e decide a próxima ação."""
        pass

    @abstractmethod
    def reiniciar(self) -> None:
        """Reinicia o estado interno do agente para um novo episódio de teste."""
        pass
