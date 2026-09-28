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


def _ler_int(mensagem: str, padrao: int, minimo: int = 1) -> int:
    """Lê um inteiro do usuário com valor padrão e validação de mínimo."""
    try:
        entrada = input(mensagem).strip()
    except (EOFError, KeyboardInterrupt):
        return padrao
    if entrada == "":
        return padrao
    try:
        valor = int(entrada)
        return valor if valor >= minimo else padrao
    except ValueError:
        return padrao


def _ler_float(mensagem: str, padrao: float) -> float:
    """Lê um float (aceita vírgula ou ponto) com valor padrão."""
    try:
        entrada = input(mensagem).strip().replace(",", ".")
    except (EOFError, KeyboardInterrupt):
        return padrao
    if entrada == "":
        return padrao
    try:
        valor = float(entrada)
        return valor if 0.0 <= valor <= 1.0 else padrao
    except ValueError:
        return padrao


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


def solicitar_configuracao_ambiente():
    """Permite ao usuário definir um tabuleiro maleável (tamanho, sujeira, obstáculos)."""
    print("\n" + "-" * 55)
    print("CONFIGURAÇÃO DO AMBIENTE (Enter = valor padrão)")
    print("-" * 55)
    largura = _ler_int("Largura da grade (colunas) [Padrão: 5]: ", 5)
    altura = _ler_int("Altura da grade (linhas)   [Padrão: 5]: ", 5)
    taxa_sujeira = _ler_float("Taxa de sujeira 0.0-1.0    [Padrão: 0.20]: ", 0.20)
    taxa_obstaculo = _ler_float("Taxa de obstáculos 0.0-1.0 [Padrão: 0.10]: ", 0.10)
    return largura, altura, taxa_sujeira, taxa_obstaculo


def main():
    configurar_terminal()
    opcao = solicitar_escolha_agente()
    largura, altura, taxa_sujeira, taxa_obstaculo = solicitar_configuracao_ambiente()

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

    # 2. Instancia o ambiente conforme configuração escolhida, robô iniciando em (0, 0)
    ambiente = Ambiente(
        largura=largura,
        altura=altura,
        taxa_sujeira=taxa_sujeira,
        taxa_obstaculo=taxa_obstaculo,
        posicao_inicial=(0, 0),
        seed=42,
    )

    # 3. Cria e orquestra a simulação até a limpeza total (sem limite fixo de passos)
    simulador = Simulador(ambiente=ambiente, agente=agente)
    relatorio = simulador.executar_simulacao(parar_ao_limpar_tudo=True, verbose=True)

    # 4. Apresenta o relatório final de avaliação
    uteis = ambiente.total_casas_uteis()
    print("\n" + "=" * 55)
    print("RELATÓRIO DE DESEMPENHO APÓS A SIMULAÇÃO")
    print("=" * 55)
    print(f"Grade:                   {largura}x{altura} ({largura * altura} células)")
    print(f"Obstáculos:              {ambiente.total_obstaculos()}")
    print(f"Passos Executados:       {relatorio['passos_totais']}")
    print(f"Total de Movimentos:     {relatorio['movimentos']}")
    print(f"Total de Aspiradas:      {relatorio['aspiradas']}")
    print(f"Sujeiras Restantes:      {relatorio['sujeiras_restantes']}")
    print(f"Casas Úteis (limpáveis): {uteis}")
    print("-" * 55)
    print(f"PONTUAÇÃO MEDIDA 1 (+1 por limpo/período): {relatorio['medida_1']}")
    print(f"PONTUAÇÃO MEDIDA 2 (+1 por limpo -1 mov):  {relatorio['medida_2']}")
    print("=" * 55)


if __name__ == "__main__":
    main()
