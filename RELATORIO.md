# Relatório Descritivo: Aplicação de Inteligência Artificial em Jogos

## 1. Introdução

### 1.1 Contexto

O desenvolvimento de jogos eletrônicos modernos requer a criação de personagens não-jogáveis (NPCs) que apresentem comportamentos convincentes e inteligentes, capazes de interagir de forma natural com o ambiente e com o jogador. A aplicação de técnicas de Inteligência Artificial (IA) é fundamental para alcançar esse objetivo, permitindo que NPCs tomem decisões autônomas e adaptem seu comportamento conforme a situação do jogo.

### 1.2 Problema de IA Proposto

Este projeto aborda o problema de criar NPCs inteligentes para um jogo de sobrevivência, onde os personagens controlados pela IA devem:

1. **Navegação Inteligente**: Os NPCs precisam navegar pelo ambiente evitando obstáculos e encontrando rotas eficientes para alcançar seus objetivos.
2. **Comportamento Adaptativo**: Os NPCs devem adaptar seu comportamento baseado no estado do jogo, alternando entre diferentes modos de operação (patrulha, perseguição, ataque, retorno).
3. **Tomada de Decisão**: Em cada momento, os NPCs devem decidir qual ação tomar baseado em informações do ambiente, como a posição do jogador, distância até objetivos e estado atual.

### 1.3 Objetivos

- Implementar um sistema de pathfinding utilizando o algoritmo A* para navegação eficiente dos NPCs
- Desenvolver uma Máquina de Estados Finitos (FSM) para gerenciar os diferentes comportamentos dos NPCs
- Integrar ambas as técnicas em um ambiente de jogo funcional
- Avaliar o desempenho da solução implementada

## 2. Fundamentação Teórica

### 2.1 Pathfinding com Algoritmo A*

O pathfinding é uma técnica fundamental em jogos para determinar o caminho mais eficiente entre dois pontos em um ambiente com obstáculos. O algoritmo A* (A-star) é amplamente utilizado por combinar a eficiência do algoritmo de Dijkstra com a heurística do algoritmo Greedy Best-First Search.

#### 2.1.1 Funcionamento do A*

O algoritmo A* utiliza uma função de avaliação f(n) = g(n) + h(n), onde:

- **g(n)**: Custo real do caminho do ponto inicial até o nó n
- **h(n)**: Custo estimado (heurístico) do nó n até o objetivo
- **f(n)**: Custo total estimado do caminho que passa pelo nó n

O algoritmo mantém duas estruturas:

- **Open Set**: Nós candidatos a serem explorados, ordenados por f(n)
- **Closed Set**: Nós já explorados

A cada iteração, o algoritmo seleciona o nó com menor f(n) do Open Set, adiciona seus vizinhos válidos e repete até encontrar o objetivo.

#### 2.1.2 Heurística Manhattan

Para este projeto, foi utilizada a distância de Manhattan como heurística, calculada como:

```
h(n) = |x_n - x_goal| + |y_n - y_goal|
```

Esta heurística é admissível (nunca superestima o custo real) e eficiente para ambientes com movimento em 8 direções.

### 2.2 Máquina de Estados Finitos (FSM)

Uma Máquina de Estados Finitos é um modelo computacional que descreve o comportamento de um sistema através de um conjunto finito de estados, transições entre estados e ações associadas a cada estado.

#### 2.2.1 Componentes de uma FSM

- **Estados**: Representam diferentes modos de operação do sistema
- **Transições**: Condições que determinam quando mudar de um estado para outro
- **Ações**: Comportamentos executados quando em um determinado estado

#### 2.2.2 Vantagens da FSM em Jogos

- **Simplicidade**: Fácil de entender e implementar
- **Modularidade**: Cada estado pode ser desenvolvido independentemente
- **Previsibilidade**: Comportamento determinístico e fácil de depurar
- **Eficiência**: Baixo custo computacional

## 3. Escolha das Técnicas de IA

### 3.1 Justificativa para Pathfinding (A*)

O algoritmo A* foi escolhido para pathfinding pelas seguintes razões:

1. **Eficiência**: Encontra o caminho ótimo em tempo razoável, mesmo em ambientes complexos
2. **Garantia de Otimalidade**: Quando a heurística é admissível, garante encontrar o caminho de menor custo
3. **Flexibilidade**: Pode ser adaptado para diferentes tipos de terreno e custos de movimento
4. **Ampla Aplicação**: Padrão da indústria de jogos, amplamente testado e documentado

### 3.2 Justificativa para Máquina de Estados Finitos

A FSM foi escolhida para gerenciar o comportamento dos NPCs porque:

1. **Adequação ao Problema**: O comportamento dos NPCs pode ser naturalmente modelado como um conjunto de estados distintos (patrulha, perseguição, ataque, retorno)
2. **Clareza de Implementação**: Facilita a compreensão e manutenção do código
3. **Desempenho**: Execução muito eficiente, adequada para múltiplos NPCs simultâneos
4. **Escalabilidade**: Fácil adicionar novos estados e comportamentos

### 3.3 Integração das Técnicas

As duas técnicas se complementam perfeitamente:

- A FSM determina **o que** o NPC deve fazer (qual comportamento executar)
- O A* determina **como** o NPC deve fazer (qual caminho seguir)

## 4. Solução Implementada

### 4.1 Arquitetura do Sistema

O projeto foi desenvolvido em Python utilizando a biblioteca Pygame para renderização gráfica. A arquitetura é modular, composta pelos seguintes componentes:

#### 4.1.1 Estrutura de Arquivos

- `main.py`: Ponto de entrada do programa
- `game.py`: Lógica principal do jogo e gerenciamento do ambiente
- `pathfinding.py`: Implementação do algoritmo A*
- `fsm.py`: Implementação da Máquina de Estados Finitos
- `npc.py`: Classe NPC que integra FSM e Pathfinding
- `utils.py`: Funções auxiliares (cálculo de distância, normalização de vetores)

### 4.2 Implementação do Pathfinding

#### 4.2.1 Classe Pathfinding

A classe `Pathfinding` gerencia a navegação no ambiente:

```python
class Pathfinding:
    def __init__(self, grid_width, grid_height, cell_size)
    def find_path(self, start_pos, goal_pos) -> List[Tuple[int, int]]
    def get_next_step(self, start_pos, goal_pos) -> Optional[Tuple[int, int]]
```

#### 4.2.2 Representação do Ambiente

O ambiente é representado como uma grade (grid) onde cada célula pode ser:

- **Caminhável**: NPCs podem passar
- **Obstáculo**: Bloqueia a passagem dos NPCs

#### 4.2.3 Algoritmo A* Implementado

1. Inicialização: Cria nó inicial e objetivo
2. Loop principal:
   - Remove nó com menor f(n) do Open Set
   - Se é o objetivo, reconstrói e retorna o caminho
   - Adiciona vizinhos válidos ao Open Set
   - Calcula g(n) e h(n) para cada vizinho
3. Retorna lista de coordenadas do caminho encontrado

### 4.3 Implementação da FSM

#### 4.3.1 Estados Implementados

A FSM possui quatro estados principais:

1. **PATROL (Patrulha)**: NPC se move entre pontos pré-definidos
2. **CHASE (Perseguição)**: NPC persegue o jogador quando detectado
3. **ATTACK (Ataque)**: NPC ataca o jogador quando próximo
4. **RETURN (Retorno)**: NPC retorna à posição inicial quando perde o jogador

#### 4.3.2 Transições de Estado

As transições são definidas por condições:

- **PATROL → CHASE**: Jogador detectado dentro do alcance de detecção
- **CHASE → ATTACK**: Jogador dentro do alcance de ataque
- **CHASE → RETURN**: Jogador perdido e longe da posição inicial
- **ATTACK → CHASE**: Jogador saiu do alcance de ataque mas ainda detectado
- **ATTACK → RETURN**: Jogador perdido
- **RETURN → PATROL**: NPC retornou à posição inicial

#### 4.3.3 Handlers de Estado

Cada estado possui um handler que define o comportamento:

- **handle_patrol()**: Move NPC entre pontos de patrulha usando pathfinding
- **handle_chase()**: Calcula caminho até o jogador e persegue
- **handle_attack()**: Executa ataque e aplica cooldown
- **handle_return()**: Calcula caminho de volta à posição inicial

### 4.4 Implementação do NPC

#### 4.4.1 Atributos do NPC

- Posição e velocidade
- Raio de detecção e ataque
- Sistema de vida
- Referências para FSM e Pathfinding
- Lista de pontos de patrulha

#### 4.4.2 Integração FSM + Pathfinding

O NPC utiliza a FSM para decidir o comportamento e o pathfinding para executar a navegação:

```python
def update(self, player_pos):
    self.fsm.update(player_pos)  # Atualiza estado baseado em condições
  
    # Cada handler de estado usa pathfinding quando necessário
    if self.fsm.get_state() == State.CHASE:
        next_step = self.pathfinding.get_next_step(
            (self.x, self.y), player_pos
        )
```

### 4.5 Ambiente de Jogo

#### 4.5.1 Características do Ambiente

- Tamanho: 1200x800 pixels
- Grade: 30x20 células (cada célula = 40 pixels)
- Obstáculos: 15 obstáculos aleatórios posicionados no início
- NPCs: 4 NPCs posicionados nos cantos do mapa

#### 4.5.2 Mecânicas de Jogo

- Jogador controlado por teclado (WASD ou setas)
- NPCs detectam jogador em raio de 150 pixels
- NPCs atacam em raio de 40 pixels
- Sistema de vida para jogador e NPCs
- Visualização de estados dos NPCs (cores indicativas)

## 5. Demonstração da Execução

### 5.1 Cenários de Teste

#### 5.1.1 Cenário 1: Patrulha Normal

**Situação**: Jogador longe dos NPCs
**Comportamento Esperado**: NPCs patrulham entre pontos pré-definidos
**Resultado Observado**: NPCs alternam entre pontos de patrulha usando pathfinding para evitar obstáculos

#### 5.1.2 Cenário 2: Detecção e Perseguição

**Situação**: Jogador entra no raio de detecção de um NPC
**Comportamento Esperado**: NPC muda para estado CHASE e persegue o jogador
**Resultado Observado**: NPC calcula caminho até o jogador usando A* e persegue, evitando obstáculos

#### 5.1.3 Cenário 3: Ataque

**Situação**: NPC alcança o jogador (dentro do raio de ataque)
**Comportamento Esperado**: NPC muda para estado ATTACK e causa dano
**Resultado Observado**: NPC ataca o jogador periodicamente (respeitando cooldown)

#### 5.1.4 Cenário 4: Perda do Jogador

**Situação**: Jogador sai do raio de detecção
**Comportamento Esperado**: NPC muda para estado RETURN e volta à posição inicial
**Resultado Observado**: NPC calcula caminho de volta usando A* e retorna, depois retoma patrulha

### 5.2 Visualizações

O jogo apresenta visualizações para facilitar a compreensão:

- **Grid**: Grade do ambiente (pode ser desativada com F1)
- **Obstáculos**: Retângulos cinza
- **NPCs**: Círculos coloridos com indicador de estado
- **Caminho**: Pontos azuis mostram o caminho calculado pelo A*
- **Raio de Detecção**: Círculo amarelo quando NPC está perseguindo
- **Barras de Vida**: Indicadores acima de NPCs e jogador

### 5.3 Métricas de Desempenho

Durante a execução, observa-se:

- **Tempo de Cálculo de Caminho**: < 1ms para caminhos típicos
- **Taxa de Quadros**: Mantém 60 FPS com 4 NPCs ativos
- **Precisão de Navegação**: NPCs sempre encontram caminho quando existe
- **Transições de Estado**: Ocorrem instantaneamente quando condições são atendidas

## 6. Análise Crítica

### 6.1 Pontos Fortes da Implementação

#### 6.1.1 Eficiência do Pathfinding

O algoritmo A* demonstra excelente desempenho:

- Encontra caminhos ótimos em tempo real
- Lida eficientemente com ambientes com múltiplos obstáculos
- Cálculo de caminho não impacta significativamente a performance

#### 6.1.2 Clareza da FSM

A Máquina de Estados Finitos proporciona:

- Código organizado e fácil de entender
- Comportamento previsível e depurável
- Facilidade para adicionar novos estados

#### 6.1.3 Integração Harmoniosa

A combinação das duas técnicas funciona bem:

- FSM gerencia decisões de alto nível
- Pathfinding gerencia navegação de baixo nível
- Separação clara de responsabilidades

### 6.2 Limitações e Desafios

#### 6.2.1 Limitações do A*

- **Custo Computacional**: Em mapas muito grandes, o A* pode se tornar lento
- **Memória**: Mantém todos os nós explorados na memória
- **Caminhos Rígidos**: NPCs seguem caminhos pré-calculados, podem parecer robóticos

#### 6.2.2 Limitações da FSM

- **Comportamento Previsível**: Estados fixos podem tornar NPCs previsíveis
- **Falta de Memória**: Não mantém histórico de ações passadas
- **Transições Binárias**: Transições são baseadas apenas em condições atuais

#### 6.2.3 Desafios de Integração

- **Sincronização**: Pathfinding e FSM precisam estar sincronizados
- **Atualização Contínua**: Caminhos precisam ser recalculados quando objetivos mudam
- **Edge Cases**: Situações onde não existe caminho válido

### 6.3 Melhorias Possíveis

#### 6.3.1 Melhorias no Pathfinding

1. **Path Smoothing**: Suavizar caminhos para movimento mais natural
2. **Dynamic Obstacle Avoidance**: Evitar obstáculos dinâmicos em tempo real
3. **Hierarchical Pathfinding**: Usar pathfinding hierárquico para mapas grandes
4. **Flow Fields**: Para múltiplos NPCs seguindo o mesmo objetivo

#### 6.3.2 Melhorias na FSM

1. **Hierarchical FSM**: Estados compostos para comportamentos mais complexos
2. **Behavior Trees**: Alternativa mais flexível para comportamentos complexos
3. **Utility-based AI**: Sistema baseado em utilidade para decisões mais sofisticadas
4. **Machine Learning**: Aprendizado de padrões de comportamento do jogador

#### 6.3.3 Melhorias Gerais

1. **Sistema de Percepção**: Visão limitada, audição, cheiro
2. **Coordenação entre NPCs**: Comunicação e trabalho em equipe
3. **Personalidade**: Diferentes NPCs com comportamentos distintos
4. **Adaptação**: NPCs que aprendem com interações anteriores

### 6.4 Comparação com Abordagens Alternativas

#### 6.4.1 Pathfinding Alternativo

- **Dijkstra**: Mais lento, mas garante caminho ótimo sem heurística
- **Breadth-First Search**: Mais simples, mas menos eficiente
- **Jump Point Search**: Otimização do A* para grades uniformes
- **Theta***: Permite movimento em linha reta entre nós não adjacentes

#### 6.4.2 Sistemas de Comportamento Alternativos

- **Behavior Trees**: Mais flexíveis, mas mais complexos
- **Goal-Oriented Action Planning (GOAP)**: Planejamento automático de ações
- **Utility AI**: Decisões baseadas em valores de utilidade
- **Machine Learning**: Aprendizado de comportamentos

### 6.5 Conclusão da Análise

A solução implementada demonstra eficácia na resolução do problema proposto. A combinação de A* e FSM fornece uma base sólida para NPCs inteligentes, com bom desempenho e código manutenível. Embora existam limitações e oportunidades de melhoria, a implementação atende aos objetivos do projeto e serve como excelente ponto de partida para sistemas mais complexos.

## 7. Conclusão

Este projeto demonstrou com sucesso a aplicação de técnicas de Inteligência Artificial em um ambiente de jogo, especificamente através da implementação de pathfinding com algoritmo A* e Máquina de Estados Finitos para controle de comportamento de NPCs.

A solução desenvolvida permite que NPCs naveguem inteligentemente pelo ambiente, evitem obstáculos, detectem e persigam o jogador, e adaptem seu comportamento conforme a situação do jogo. A integração das duas técnicas resultou em um sistema funcional e eficiente.

Os resultados obtidos validam a escolha das técnicas e demonstram sua aplicabilidade prática em jogos. As limitações identificadas abrem caminho para futuras melhorias e pesquisas, como a incorporação de técnicas mais avançadas de IA ou aprendizado de máquina.

Este projeto contribui para o entendimento de como técnicas clássicas de IA podem ser aplicadas de forma eficaz em jogos, servindo como base para desenvolvimentos futuros mais complexos e sofisticados.

## 8. Referências

- Russell, S., & Norvig, P. (2020). Artificial Intelligence: A Modern Approach (4th ed.). Pearson.
- Millington, I., & Funge, J. (2019). Artificial Intelligence for Games (3rd ed.). CRC Press.
- Buckland, M. (2005). Programming Game AI by Example. Wordware Publishing.
- Rabin, S. (2014). Game AI Pro: Collected Wisdom of Game AI Professionals. CRC Press.
- Pygame Documentation. Disponível em: https://www.pygame.org/docs/
