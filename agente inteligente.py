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
