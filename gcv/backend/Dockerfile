FROM python:3.12-slim

WORKDIR /app

# Copiar apenas o requirements.txt primeiro para aproveitar o cache do Docker
COPY ./app/requirements.txt .

# Instalar as dependências
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Copiar todo o código da aplicação
COPY ./app/ .

# Expor a porta e definir o CMD padrão
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
