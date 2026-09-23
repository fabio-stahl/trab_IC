class robo:
    def __init__(self, local, estado,pontuacao):
        self.local = local
        self.estado = estado
        self.pontuacao = pontuacao  
        self.historico = []

    def guardar_local(self,local,estado):
        jogada = (local, estado)
        self.historico.append(jogada)

    def prox_movimento(self):
        ...
    