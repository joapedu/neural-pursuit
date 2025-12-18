# Instruções de Uso - Neural Pursuit

## Instalação

1. Certifique-se de ter Python 3.8 ou superior instalado
2. Instale as dependências:
```bash
pip install -r requirements.txt
```

## Execução

Execute o jogo com:
```bash
python main.py
```

## Controles

- **W, A, S, D** ou **Setas do Teclado**: Mover o jogador
- **ESC**: Sair do jogo
- **F1**: Alternar visualização da grade (debug)

## Como Funciona

### NPCs e seus Estados

Os NPCs possuem 4 estados diferentes, indicados por cores:

1. **Verde (PATROL)**: NPC está patrulhando entre pontos pré-definidos
2. **Amarelo (CHASE)**: NPC detectou o jogador e está perseguindo
3. **Vermelho (ATTACK)**: NPC está próximo o suficiente para atacar
4. **Azul (RETURN)**: NPC perdeu o jogador e está retornando à posição inicial

### Sistema de Pathfinding

- Os NPCs usam o algoritmo A* para encontrar caminhos
- Pontos azuis mostram o caminho calculado
- NPCs evitam obstáculos automaticamente

### Sistema de Detecção

- NPCs detectam o jogador em um raio de 150 pixels
- Quando perseguindo, um círculo amarelo indica o raio de detecção
- NPCs atacam quando o jogador está a menos de 40 pixels

## Estrutura do Código

### pathfinding.py
Implementa o algoritmo A* para encontrar caminhos ótimos entre dois pontos.

### fsm.py
Implementa a Máquina de Estados Finitos para gerenciar comportamentos.

### npc.py
Classe NPC que integra FSM e Pathfinding para criar comportamentos inteligentes.

### game.py
Lógica principal do jogo, gerenciamento do ambiente e renderização.

### utils.py
Funções auxiliares para cálculos matemáticos.

## Personalização

### Ajustar Parâmetros dos NPCs

No arquivo `npc.py`, você pode modificar:

- `self.speed`: Velocidade de movimento (padrão: 2.0)
- `self.detection_range`: Raio de detecção do jogador (padrão: 150)
- `self.attack_range`: Raio de ataque (padrão: 40)
- `self.health`: Vida inicial do NPC (padrão: 100)

### Adicionar Mais NPCs

No arquivo `game.py`, método `setup_npcs()`, adicione mais posições:

```python
positions = [
    (200, 200),
    (1000, 200),
    (200, 600),
    (1000, 600),
    (600, 400),  # Novo NPC
]
```

### Modificar Obstáculos

No arquivo `game.py`, método `setup_obstacles()`, ajuste:

- `num_obstacles`: Número de obstáculos (padrão: 15)

## Troubleshooting

### Problema: Jogo não inicia
- Verifique se todas as dependências estão instaladas
- Certifique-se de estar usando Python 3.8+

### Problema: NPCs não se movem
- Verifique se há caminho válido (sem obstáculos bloqueando completamente)
- NPCs podem estar em estado RETURN aguardando retornar à posição inicial

### Problema: Performance baixa
- Reduza o número de NPCs
- Desative a visualização da grade (F1)
- Reduza o número de obstáculos

