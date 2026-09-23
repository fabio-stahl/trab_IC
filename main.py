from ambiente import Ambiente
from agente_reativo_simples import AgenteReativoSimples
from simulador import Simulador

def main():
    print("=" * 55)
    print("PROJETO 1 - IA: SIMULAÇÃO DO AGENTE REATIVO SIMPLES")
    print("=" * 55)

    # 1. Instancia o ambiente 5x5 com 20% de sujeira e robô iniciando em (0, 0)
    ambiente = Ambiente(largura=5, altura=5, taxa_sujeira=0.20, posicao_inicial=(0, 0), seed=42)

    # 2. Instancia o agente reativo simples orientado por regras condição-ação
    agente = AgenteReativoSimples(seed=42)

    # 3. Cria e orquestra a simulação por 20 períodos
    simulador = Simulador(ambiente=ambiente, agente=agente)
    relatorio = simulador.executar_simulacao(total_passos=20, verbose=True)

    # 4. Apresenta o relatório final de avaliação
    print("\n" + "=" * 55)
    print("RELATÓRIO DE DESEMPENHO APÓS A SIMULAÇÃO")
    print("=" * 55)
    print(f"Passos Executados:       {relatorio['passos_totais']}")
    print(f"Total de Movimentos:     {relatorio['movimentos']}")
    print(f"Total de Aspiradas:      {relatorio['aspiradas']}")
    print(f"Sujeiras Restantes:      {relatorio['sujeiras_restantes']}/25")
    print("-" * 55)
    print(f"PONTUAÇÃO MEDIDA 1 (+1 por limpo/período): {relatorio['medida_1']}")
    print(f"PONTUAÇÃO MEDIDA 2 (+1 por limpo -1 mov):  {relatorio['medida_2']}")
    print("=" * 55)

if __name__ == "__main__":
    main()
