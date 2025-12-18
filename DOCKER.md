# Guia de Dockerização

Este documento explica como executar o projeto usando Docker.

## Pré-requisitos

- Docker instalado
- Docker Compose instalado (opcional, mas recomendado)
- No Linux: X11 server rodando (para exibir a janela do jogo)

## Métodos de Execução

### Método 1: Docker Compose (Recomendado)

#### Linux com Display

1. Permita acesso ao display X11:
```bash
xhost +local:docker
```

2. Construa e execute:
```bash
docker-compose build
docker-compose up
```

3. Ou use o script auxiliar:
```bash
./run-docker.sh
```

#### Windows/Mac

No Windows e Mac, o Docker Desktop gerencia o display automaticamente:
```bash
docker-compose build
docker-compose up
```

### Método 2: Docker Direto

#### Com Display (Linux)

```bash
xhost +local:docker
docker build -t ia-jogos .
docker run -it --rm \
  -e DISPLAY=$DISPLAY \
  -v /tmp/.X11-unix:/tmp/.X11-unix:rw \
  --network host \
  ia-jogos
```

#### Headless (sem display)

Útil para testes automatizados ou servidores sem interface gráfica:

```bash
docker build -f Dockerfile.headless -t ia-jogos-headless .
docker run -it --rm ia-jogos-headless
```

## Solução de Problemas

### Erro: "Cannot connect to X server"

**Linux:**
```bash
xhost +local:docker
export DISPLAY=:0
```

**Verificar se X11 está rodando:**
```bash
echo $DISPLAY
```

### Erro: "Permission denied" no X11

Execute:
```bash
xhost +local:docker
```

Ou adicione seu usuário ao grupo docker:
```bash
sudo usermod -aG docker $USER
newgrp docker
```

### Performance lenta

Se o jogo estiver lento dentro do container:
- Use `--network host` (já incluído no docker-compose.yml)
- Certifique-se de ter drivers gráficos atualizados
- Considere usar a versão headless para testes

### Container não inicia

Verifique os logs:
```bash
docker-compose logs
```

Ou para container individual:
```bash
docker logs ia-jogos
```

## Estrutura dos Arquivos Docker

- **Dockerfile**: Para execução com display gráfico
- **Dockerfile.headless**: Para execução sem display (usa Xvfb)
- **docker-compose.yml**: Orquestração simplificada
- **.dockerignore**: Arquivos excluídos da imagem

## Desenvolvimento com Docker

Para desenvolvimento, monte o código como volume:

```bash
docker run -it --rm \
  -e DISPLAY=$DISPLAY \
  -v /tmp/.X11-unix:/tmp/.X11-unix:rw \
  -v $(pwd):/app \
  --network host \
  ia-jogos
```

Isso permite editar o código localmente e ver mudanças no container.

## Limpeza

Remover imagens e containers:

```bash
docker-compose down
docker rmi ia-jogos
```

Remover tudo relacionado ao projeto:

```bash
docker-compose down --rmi all
```

