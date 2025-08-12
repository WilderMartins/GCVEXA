# GCVEXA - Gestão Centralizada de Vulnerabilidades

O GCVEXA é uma plataforma de código aberto para a gestão centralizada de vulnerabilidades de segurança. Ele permite que você importe os resultados de escaneamentos de diversas ferramentas de segurança, centralize as informações em um único local e gerencie o ciclo de vida das vulnerabilidades.

## Funcionalidades

- **Centralização de Vulnerabilidades**: Importe os resultados de escaneamentos de ferramentas como o BurpSuite, Greenbone, SonarQube, etc.
- **Gestão do Ciclo de Vida**: Acompanhe o status de cada vulnerabilidade, desde a sua descoberta até a sua correção.
- **Visualização de Dados**: Visualize as informações de vulnerabilidades em dashboards e relatórios.
- **API para Integração**: Integre o GCVEXA com outras ferramentas e sistemas através da sua API RESTful.

## Arquitetura

O GCVEXA é composto por dois componentes principais:

- **Backend**: Uma API RESTful desenvolvida em Python com o framework FastAPI.
- **Frontend**: Uma aplicação web desenvolvida em JavaScript com a biblioteca React.

## Como Começar

Para começar a usar o GCVEXA, siga os seguintes passos:

1.  **Clone o repositório**:

    ```bash
    git clone https://github.com/seu-usuario/gcvexa.git
    ```

2.  **Inicie o ambiente de desenvolvimento**:

    ```bash
    cd gcvexa
    ./setup.sh
    ```

3.  **Acesse a aplicação**:

    - Frontend: `http://localhost:5173`
    - Backend API: `http://localhost:8000`
    - Documentação da API: `http://localhost:8000/docs`

## Como Importar Vulnerabilidades

Para importar as vulnerabilidades de uma ferramenta de escaneamento, você pode usar o seguinte endpoint da API:

`POST /api/v1/scans/import`

**Exemplo de Payload**:

```json
{
  "name": "Escaneamento do BurpSuite",
  "asset_id": 1,
  "vulnerabilities": [
    {
      "name": "SQL Injection",
      "description": "A aplicação está vulnerável a ataques de SQL Injection.",
      "severity": "Alta",
      "remediation": "Use prepared statements para evitar a concatenação de strings na construção de queries SQL.",
      "status": "Aberta"
    }
  ]
}
```

## Contribuição

Contribuições são bem-vindas! Se você deseja contribuir com o projeto, por favor, abra uma issue ou envie um pull request.
