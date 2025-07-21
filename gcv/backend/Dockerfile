FROM python:3.10-slim-buster

# WORKDIR define o diretório de execução E o adiciona ao PYTHONPATH
WORKDIR /app

# Copiar o requirements.txt para /app/requirements.txt
COPY ./app/requirements.txt .

# Instalar as dependências
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Copiar toda a pasta 'app' do host para dentro do WORKDIR,
# resultando em uma estrutura /app/main.py, /app/db/, etc.
COPY ./app/ .

EXPOSE 8000

# O comando será executado a partir de /app.
# O uvicorn precisa ser informado do módulo a ser executado: app.main
# Como o WORKDIR é /app, o Python procurará por /app/app/main.py
# Isso está errado. O comando deve ser uvicorn main:app
# E o código deve estar na raiz do WORKDIR.

# --- Correção Definitiva ---

# WORKDIR será a raiz do nosso código
WORKDIR /gcv_app

# Copiar o requirements.txt para a raiz
COPY ./app/requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Copiar a pasta 'app' inteira para dentro do WORKDIR
# Agora teremos a estrutura /gcv_app/app/main.py
COPY ./app ./app

EXPOSE 8000

# O comando agora é executado a partir de /gcv_app
# E ele pode encontrar o pacote 'app'
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
