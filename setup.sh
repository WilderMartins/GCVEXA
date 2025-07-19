#!/bin/bash

# Cores para o output
GREEN='\033[0;32m'
NC='\033[0m' # No Color

echo -e "${GREEN}Iniciando o setup do ambiente GCV...${NC}"

# 1. Verificar se o Docker está em execução
if ! docker info > /dev/null 2>&1; then
  echo "Erro: O Docker não parece estar em execução. Por favor, inicie o Docker e tente novamente."
  exit 1
fi

# 2. Construir as imagens Docker
echo -e "${GREEN}Construindo as imagens Docker (isso pode levar alguns minutos)...${NC}"
docker-compose build
if [ $? -ne 0 ]; then
    echo "Erro: Falha ao construir as imagens Docker. Verifique os logs acima."
    exit 1
fi


# 3. Iniciar os contêineres em modo detached
echo -e "${GREEN}Iniciando os serviços com Docker Compose...${NC}"
docker-compose up -d
if [ $? -ne 0 ]; then
    echo "Erro: Falha ao iniciar os contêineres. Verifique os logs com 'docker-compose logs'."
    exit 1
fi


# 4. Mensagem de sucesso
echo -e "${GREEN}Ambiente GCV iniciado com sucesso!${NC}"
echo "----------------------------------------"
echo "Frontend (React): http://localhost:5173"
echo "Backend API (FastAPI): http://localhost:8000"
echo "Documentação da API (Swagger): http://localhost:8000/docs"
echo "----------------------------------------"
echo "Para parar o ambiente, execute: docker-compose down"
