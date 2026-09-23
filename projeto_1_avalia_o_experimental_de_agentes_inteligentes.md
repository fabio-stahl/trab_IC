# Projeto 1 - Avaliação Experimental de Agentes Inteligentes

## Objetivos

1. Compreender os conceitos fundamentais necessários à aplicação da noção de agentes inteligentes na resolução de problemas em ambientes de tarefas de diversos tipos.
2. Projetar programas de agentes artificiais reativos simples e reativos baseados em modelos, orientados por regras condição-ação, para resolver problemas em ambientes de tarefas determinísticos e parcialmente observáveis.
3. Avaliar o desempenho de agentes inteligentes em ambientes de tarefas simulados em computador.

## Justificativas

**Qual a importância do estudo dos conceitos sobre agentes inteligentes, do projeto, e da avaliação de desempenho de agentes reativos simples e baseados em modelos?**

* O ponto de vista de agentes abrange muitas entidades no mundo, ou seja, que podem ser vistas como interagindo com um ambiente por meio de sensores e atuadores, visando realizar algum objetivo.
* A grande maioria dos sistemas computacionais são agentes artificiais concebidos para realizar objetivos em ambientes parcialmente observáveis.
* Alguns dos sistemas computacionais agentes artificiais são concebidos como agentes reativos que tomam decisões baseados em percepções do ambiente e regras condição-ação. Outros sistemas são concebidos como agentes baseados em modelos, isto é, que tomam decisões considerando um estado interno a respeito do ambiente e um conjunto de regras condição-ação.
* A definição de inteligência artificial (IA) moderna considera um conceito ideal de inteligência, ou seja, a noção de racionalidade. Considerando este ponto de vista, o projetista do agente artificial precisa avaliar o desempenho do sistema e verificar se ele é inteligente, ou seja, se o agente artificial é racional. A avaliação de desempenho deve ser realizada de maneira adequada visando perceber se o agente tem a capacidade de realizar o objetivo para o qual foi projetado.

## Metodologia

Para realizar os objetivos do projeto: implementar um programa de agente artificial reativo simples e outro baseado em modelos para o ambiente de tarefas de um aspirador de pó, que é determinístico e parcialmente observável. Os agentes não conhecem o padrão inicial de sujeira, nem a geografia (extensão, limites e obstáculos) do ambiente. Os sensores dos agentes percebem localmente o ambiente.

Considerar duas medidas de avaliação para os agentes: medida oferece o prêmio de um ponto para cada quadrado limpo em cada período, e medida oferece o prêmio de um ponto para cada quadrado limpo e penaliza com um ponto a menos cada movimento.

Experimentar: fixe o tamanho do ambiente e execute o agente para várias configurações iniciais possíveis de sujeira, obstáculos e posições dos agentes. Registre a pontuação de desempenho dos agentes para cada configuração do ambiente e sua pontuação média global.

Ao final do desenvolvimento do projeto: conceber apresentação (máximo 10 min) descrevendo os mecanismos de atualização de estado interno e de tomada de decisão de cada agente, uma breve descrição do comportamento de cada agente, tabelas, gráficos e uma análise dos resultados a partir do ponto de vista da racionalidade de cada programa.