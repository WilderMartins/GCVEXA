# Usar uma imagem base oficial do Node.js
FROM node:20-alpine

# Definir o diretório de trabalho no contêiner
WORKDIR /app

# Copiar o package.json e package-lock.json para o diretório de trabalho
# Isso aproveita o cache do Docker, reinstalando dependências apenas se esses arquivos mudarem
COPY package*.json ./

# Instalar as dependências do projeto
RUN npm install

# Copiar todo o código do frontend para o diretório de trabalho
COPY . .

# Expor a porta que o Vite irá rodar
EXPOSE 5173

# Comando para iniciar o servidor de desenvolvimento do Vite
# O --host permite que o servidor seja acessível de fora do contêiner
CMD ["npm", "run", "dev", "--", "--host"]
