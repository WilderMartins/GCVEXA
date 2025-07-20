# GCV - Sistema de Gestão de Vulnerabilidades

## 1. Visão Geral (Objective)


O **Sistema de Gestão de Vulnerabilidades (GCV)** é uma plataforma SaaS projetada para agregar, orquestrar e remediar vulnerabilidades de segurança de forma centralizada e inteligente. O sistema é construído para ser multitenant e customizável (whitelabel), permitindo que diferentes organizações o utilizem de forma isolada.

O GCV se integra a uma variedade de scanners de segurança (Infraestrutura, DAST, SAST) para consolidar os resultados em um único dashboard, fornecendo métricas executivas e técnicas para ajudar as equipes a priorizar e corrigir falhas de segurança de forma eficiente.


## 2. Arquitetura

O GCV utiliza uma arquitetura de microsserviços lógicos dentro de um monorepo, containerizada com Docker.

-   **Monorepo:** O código-fonte para o backend e o frontend reside no mesmo repositório, simplificando o desenvolvimento e o versionamento.
-   **Backend:** Uma API robusta construída com **Python** e **FastAPI**, responsável pela lógica de negócio, autenticação, orquestração de scans e comunicação com o banco de dados.
-   **Frontend:** Uma Single Page Application (SPA) moderna construída com **React** e **Vite**, fornecendo uma interface de usuário reativa e intuitiva.
-   **Banco de Dados:** **PostgreSQL** é usado para a persistência de dados relacionais complexos, como usuários, configurações de scanner, scans e vulnerabilidades.
-   **Scanners:** O sistema se integra a scanners externos, que são executados como serviços separados (ex: OpenVAS, ZAP) ou como processos sob demanda (ex: Semgrep).
-   **Containerização:** Todos os serviços principais (backend, frontend, banco de dados, ZAP, SonarQube) são definidos no `docker-compose.yml` para fácil orquestração em desenvolvimento e implantação em servidor único.

## 3. Setup de Desenvolvimento

### Pré-requisitos
-   Docker
-   Docker Compose
-   Git

### Instruções de Instalação

1.  **Clonar o Repositório**

    ```bash
    git clone <URL_DO_REPOSITORIO>
    cd gcv
    ```


2.  **Configurar Variáveis de Ambiente**
    O GCV precisa de um arquivo de configuração para o backend. Copie o arquivo de exemplo e preencha as chaves de API necessárias.
    ```bash
    cp gcv/backend/app/.env.example gcv/backend/app/.env
    ```
    Edite o arquivo `gcv/backend/app/.env` e preencha os seguintes valores:
    -   `GEMINI_API_KEY`: Sua chave de API do Google Gemini.
    -   `GOOGLE_CLIENT_ID` e `GOOGLE_CLIENT_SECRET`: Suas credenciais OAuth do Google.
    -   (Opcional) Configurações de SMTP para envio de e-mail.

3.  **Executar o Script de Setup**
    O script `setup.sh` irá construir as imagens Docker e iniciar todos os serviços.

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

Para executar os testes do frontend, entre no diretório e use o script de teste do npm.

```bash
cd gcv/frontend
npm test
```
