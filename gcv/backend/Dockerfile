# Usar uma imagem base oficial do Python
FROM python:3.12-slim

# Definir o diretório de trabalho no contêiner
WORKDIR /app

# Copiar o arquivo de dependências e instalar
# Isso é feito em um passo separado para aproveitar o cache do Docker
COPY ./app/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

# Copiar o código da aplicação para o diretório de trabalho
# O conteúdo de 'gcv/backend/app' será copiado para '/app' no contêiner
COPY ./app /app

# Expor a porta que o Uvicorn irá rodar
EXPOSE 8000

# O comando para iniciar a aplicação é definido no docker-compose.yml,
# mas ter um CMD padrão é uma boa prática.
# Uvicorn será executado a partir de /app, então ele encontrará 'app.main'.
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
