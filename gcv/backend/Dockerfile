# Usar uma imagem base oficial do Python
FROM python:3.12-slim

# Definir o diretório de trabalho no contêiner
WORKDIR /app

# Instalar as dependências
COPY app/requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Copiar o código da aplicação
COPY app/ .

# Expor a porta que o Uvicorn irá rodar
EXPOSE 8000

# O comando para iniciar a aplicação é definido no docker-compose.yml
# CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
