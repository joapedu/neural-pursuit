# Neural Pursuit

## Description

**Neural Pursuit** is a survival game where NPCs (Non-Player Characters) use Artificial Intelligence techniques to navigate and interact with the environment. The implemented techniques include:

- **Finite State Machine (FSM)**: To manage complex NPC behaviors
- __Pathfinding (A*)__: For intelligent navigation in environments with obstacles

## Installation

### Method 1: Local Installation

```bash
pip install -r requirements.txt
```

### Method 2: Docker

```bash
docker-compose build
```

## Execution

### Method 1: Local Execution

```bash
python main.py
```

### Method 2: Docker Execution

**Linux:**
```bash
xhost +local:docker
docker-compose up
```

**Or using Docker directly:**
```bash
xhost +local:docker
docker build -t ia-jogos .
docker run -it --rm \
  -e DISPLAY=$DISPLAY \
  -v /tmp/.X11-unix:/tmp/.X11-unix:rw \
  --network host \
  ia-jogos
```

**Note:** On Linux, you need to allow X11 display access. Run `xhost +local:docker` before running the container.

## Controls

- **WASD** or **Arrow Keys**: Move the player
- **ESC**: Exit game (or return to menu if playing)
- **F1**: Toggle grid visualization (debug)
- **SPACE**: Start game from menu

## Project Structure

- `main.py`: Main game file
- `game.py`: Main game logic and rendering
- `pathfinding.py`: A* algorithm implementation for pathfinding
- `fsm.py`: Finite State Machine implementation
- `npc.py`: NPC class with FSM and Pathfinding integration
- `graphics.py`: Graphics system and visual effects
- `sprites_manager.py`: Sprite loading and management system
- `utils.py`: Helper functions
- `Dockerfile`: Docker configuration for display execution
- `Dockerfile.headless`: Docker configuration for headless execution
- `docker-compose.yml`: Docker Compose configuration
- `run-docker.sh`: Helper script to run with Docker

## Headless Execution (no display)

To run without graphical interface (useful for automated testing):

```bash
docker build -f Dockerfile.headless -t ia-jogos-headless .
docker run -it --rm ia-jogos-headless
```
