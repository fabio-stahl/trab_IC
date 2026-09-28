from agente_reativo_simples import AgenteReativoSimples
from tipos import Acao, Percepcao

# Alias para compatibilidade com o esboço inicial
RoboReativoSimples = AgenteReativoSimples

try:
    from agente_inteligente import AgenteBaseadoEmModelo
    RoboBaseadoEmModelo = AgenteBaseadoEmModelo
    RoboInteligente = AgenteBaseadoEmModelo
except ImportError:
    pass