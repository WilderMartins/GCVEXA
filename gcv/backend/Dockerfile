# Usar uma imagem base do Python
FROM python:3.10-slim-buster

# Definir o diretório de trabalho como /app
WORKDIR /app

# Copiar o arquivo de dependências
COPY ./app/requirements.txt /app/requirements.txt

# Instalar as dependências
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Copiar todo o código da aplicação para o WORKDIR
COPY ./app /app

# Expor a porta 8000 para permitir a comunicação com o container
EXPOSE 8000

# Comando para iniciar a aplicação com uvicorn
# Ele irá procurar por um objeto 'app' no módulo 'main.py'
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
