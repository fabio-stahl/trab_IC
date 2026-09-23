import random

class ambiente:
    def __init__(self):
        self.casas = [["LIMPO" for _ in range(5)] for _ in range(5)]

    def colocar_sujeira(self):
        i = 0
        while i < 3:
            linha = random.randint(0,4)
            coluna = random.randint(0,4)
            if self.casas[linha][coluna] == "SUJO":
                continue
            self.casas[linha][coluna] = "SUJO"
            i+=1

    