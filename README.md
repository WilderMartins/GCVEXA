# GCV - Sistema de Gestão de Vulnerabilidades
# by Martins @ 2025

## 1. Visão Geral (Objective)

O **Sistema de Gestão de Vulnerabilidades (GCV)** é uma plataforma SaaS projetada para agregar, orquestrar e remediar vulnerabilidades de segurança de forma centralizada e inteligente. O sistema se integra a uma variedade de scanners de segurança (Infraestrutura, DAST, SAST) para consolidar os resultados em um único dashboard, fornecendo métricas e playbooks de automação.

## 2. Arquitetura

O GCV utiliza uma arquitetura de microsserviços lógicos dentro de um monorepo, containerizada com Docker.

-   **Backend:** API em **Python/FastAPI**.
-   **Frontend:** SPA em **React/Vite**.
-   **Banco de Dados:** **PostgreSQL** para o GCV e para o SonarQube.
-   **Containerização:** Todos os serviços (backend, frontend, bancos de dados, ZAP, SonarQube) são definidos no `docker-compose.yml`.

## 3. Guia de Instalação Rápida (Wizard)

O GCV possui um wizard de instalação web para a configuração inicial.

1.  **Pré-requisitos:**
    -   Docker
    -   Docker Compose
    -   Git

2.  **Clone o Repositório**
    ```bash
    git clone <URL_DO_REPOSITORIO>
    cd gcv
    ```

3.  **Inicie os Serviços**
    O script `setup.sh` irá construir e iniciar todos os contêineres Docker.
    ```bash
    chmod +x setup.sh
    ./setup.sh
    ```
    *Aguarde alguns minutos, pois o SonarQube pode demorar para iniciar.*

4.  **Acesse o Wizard de Instalação**
    Abra seu navegador e acesse: `http://localhost:5173`

    Você será automaticamente redirecionado para o wizard de instalação, onde criará a conta de Administrador.

5.  **Login**
    Após completar o wizard, você será redirecionado para a página de login. Use as credenciais que acabou de criar.

## 4. Configuração Avançada (Opcional)

Para habilitar funcionalidades que dependem de serviços externos, você precisará configurar as variáveis de ambiente.

1.  Crie um arquivo `.env` no diretório `gcv/backend/app/` (você pode copiar o `.env.example`).
2.  Edite o arquivo e adicione as seguintes chaves:

    -   **`GEMINI_API_KEY`**: Necessária para a funcionalidade "Resumir com IA".
    -   **`GOOGLE_CLIENT_ID` / `GOOGLE_CLIENT_SECRET`**: Necessárias para o Login Social com Google.
    -   **Configurações de SMTP**: Necessárias para o envio de notificações por e-mail.

## 5. Executando os Testes

### Testes do Backend
```bash
cd gcv/backend
pytest
```

### Testes do Frontend
```bash
cd gcv/frontend
npm test
```
