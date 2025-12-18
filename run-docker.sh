#!/bin/bash

echo "Configurando acesso ao display X11..."
xhost +local:docker 2>/dev/null || echo "Aviso: xhost pode não estar disponível"

echo "Construindo imagem Docker..."
docker-compose build

echo "Iniciando o jogo..."
docker-compose up

