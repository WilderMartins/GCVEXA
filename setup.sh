#!/bin/bash

# Cores para o output
GREEN='\033[0;32m'
NC='\033[0m' # No Color
YELLOW='\033[1;33m'

# Função para verificar o status do Docker
check_docker() {
    if ! docker info > /dev/null 2>&1; then
        echo "Erro: O Docker não parece estar em execução. Por favor, inicie o Docker e tente novamente."
        exit 1
    fi
}

# Determinar o ambiente
ENV=$1
COMPOSE_FILE="docker-compose.yml"

if [ "$ENV" == "prod" ]; then
    echo -e "${YELLOW}Executando em modo de PRODUÇÃO${NC}"
    COMPOSE_FILE="docker-compose.prod.yml"
elif [ "$ENV" == "dev" ] || [ -z "$ENV" ]; then
    echo -e "${YELLOW}Executando em modo de DESENVOLVIMENTO${NC}"
    ENV="dev" # Garante que a variável não esteja vazia
else
    echo "Erro: Argumento inválido. Use 'dev' ou 'prod'."
    exit 1
fi

echo -e "${GREEN}Iniciando o setup do ambiente GCV (${ENV})...${NC}"

# 1. Verificar o Docker
check_docker

# 2. Construir as imagens Docker
echo -e "${GREEN}Construindo as imagens Docker (isso pode levar alguns minutos)...${NC}"
docker-compose -f ${COMPOSE_FILE} build
if [ $? -ne 0 ]; then
    echo "Erro: Falha ao construir as imagens Docker. Verifique os logs acima."
    exit 1
fi

# 3. Iniciar os contêineres em modo detached
echo -e "${GREEN}Iniciando os serviços com Docker Compose...${NC}"
docker-compose -f ${COMPOSE_FILE} up -d
if [ $? -ne 0 ]; then
    echo "Erro: Falha ao iniciar os contêineres. Verifique os logs com 'docker-compose -f ${COMPOSE_FILE} logs'."
    exit 1
fi

# 4. Mensagem de sucesso
echo -e "${GREEN}Ambiente GCV (${ENV}) iniciado com sucesso!${NC}"
echo "----------------------------------------"
if [ "$ENV" == "prod" ]; then
    echo "Aplicação disponível em: http://localhost"
else
    echo "Frontend (React): http://localhost:5173"
    echo "Backend API (FastAPI): http://localhost:8000"
    echo "Documentação da API (Swagger): http://localhost:8000/docs"
fi
echo "----------------------------------------"
echo "Para parar o ambiente, execute: docker-compose -f ${COMPOSE_FILE} down"
