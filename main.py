import sys
from ambiente import Ambiente
from agente_reativo_simples import AgenteReativoSimples
from agente_inteligente import AgenteBaseadoEmModelo
from simulador import Simulador

def configurar_terminal():
    """Garante compatibilidade de encoding UTF-8 no terminal Windows."""
    if sys.platform == "win32":
        try:
            sys.stdout.reconfigure(encoding="utf-8")
            sys.stderr.reconfigure(encoding="utf-8")
        except Exception:
            pass

def solicitar_escolha_agente():
    """Solicita interativamente ao usuário qual robô deseja simular."""
    print("=" * 55)
    print("PROJETO 1 - IA: SIMULAÇÃO DE AGENTES INTELIGENTES")
    print("=" * 55)
    print("Escolha o agente para a simulação:")
    print("1 - Agente Reativo Simples (sem memória / reflexo)")
    print("2 - Agente Baseado em Modelo (inteligente / com memória)")
    print("-" * 55)

    # Suporta argumento por linha de comando (ex: python main.py 2)
    if len(sys.argv) > 1 and sys.argv[1] in ("1", "2"):
        opcao = sys.argv[1]
        print(f"Opção selecionada via argumento: {opcao}")
        return opcao

    while True:
        try:
            entrada = input("Digite a opção desejada (1 ou 2) [Padrão: 1]: ").strip()
            if entrada == "" or entrada == "1":
                return "1"
            if entrada == "2":
                return "2"
            print("Opção inválida! Por favor, digite 1 ou 2.")
        except (EOFError, KeyboardInterrupt):
            print("\nEntrada encerrada. Utilizando opção padrão (1).")
            return "1"

def main():
    configurar_terminal()
    opcao = solicitar_escolha_agente()

    # 1. Configura o agente e título da simulação com base na escolha
    if opcao == "1":
        nome_agente = "AGENTE REATIVO SIMPLES"
        agente = AgenteReativoSimples(seed=42)
    else:
        nome_agente = "AGENTE BASEADO EM MODELO"
        agente = AgenteBaseadoEmModelo(seed=42)

    print("\n" + "=" * 55)
    print(f"PROJETO 1 - IA: SIMULAÇÃO DO {nome_agente}")
    print("(Critério de parada: quando limpar todas as sujeiras)")
    print("=" * 55)

    # 2. Instancia o ambiente 5x5 com 20% de sujeira e robô iniciando em (0, 0)
    ambiente = Ambiente(largura=5, altura=5, taxa_sujeira=0.20, posicao_inicial=(0, 0), seed=42)

    # 3. Cria e orquestra a simulação até a limpeza total (sem limite fixo de passos)
    simulador = Simulador(ambiente=ambiente, agente=agente)
    relatorio = simulador.executar_simulacao(parar_ao_limpar_tudo=True, verbose=True)



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
