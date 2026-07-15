# MemoHub

> Sua base pessoal de conhecimento estruturada em Pergunta → Resposta.

O **MemoHub** é uma aplicação web projetada para centralizar, organizar e recuperar informações importantes com rapidez. Diferente de um aplicativo de notas convencional, o sistema foca no formato pragmático de **Pergunta → Resposta**, funcionando como um repositório dinâmico para dúvidas resolvidas, evitando retrabalho em pesquisas futuras.

---

## Estrutura do Repositório (Monorepo)

O ecossistema adota uma arquitetura de Monorepo unificada, separando os códigos das aplicações, bibliotecas compartilhadas e scripts automatizados de provisionamento e infraestrutura.

```text
meu-projeto-monorepo/
├── .github/                 # Workflows de CI/CD (GitHub Actions)
├── apps/                    # Aplicações em si
│   ├── backend/             # Código da sua API (FastAPI)
│   └── frontend/            # Código da interface (Vue 3)
├── packages/                # Bibliotecas ou pacotes compartilhados
└── infra/                   # Infraestrutura e Configuração
    ├── terraform/           # Scripts de provisionamento de cloud (AWS)
    └── ansible/             # Playbooks para configuração de servidores
```

---

## Funcionalidades

* **Gerenciamento de Conhecimento:** Criação, leitura, atualização e exclusão (CRUD) de registros.
* **Busca Avançada:** Pesquisa textual por termos contidos no título ou na pergunta.
* **Filtro por Contexto:** Organização e filtragem por categorias de assunto.
* **Favoritos:** Sistema para marcar e desmarcar registros de alta relevância de forma atômica.
* **Ordenação Cronológica:** Listagem automática priorizando registros mais recentes.

---

## Exemplos Práticos

| Categoria | Pergunta | Resposta |
| :--- | :--- | :--- |
| Programação | Como criar uma rota GET utilizando FastAPI? | Utilize o decorador `@app.get()` para definir uma rota que responda às requisições HTTP GET. |
| Culinária | Qual a proporção entre arroz e água? | Geralmente utiliza-se uma medida de arroz para duas medidas de água. |

---

## Stack Tecnológica

### Backend
[Para saber mais](./apps/backend/README.md)

### Frontend
[Para saber mais](./apps/frontend/README.md)

### Infraestrutura & DevOps
[Para saber mais](./apps/backend/README.md)

---

## Arquitetura do Sistema

A infraestrutura utiliza o **Nginx** atuando como servidor de arquivos e Proxy Reverso na ponta de entrada da máquina virtual, gerenciando o tráfego de rede e roteando as requisições HTTP de forma segura para os containers internos.

```mermaid
graph TD
    classDef client fill:#e1f5fe,stroke:#0288d1,stroke-width:2px,color:#01579b;
    classDef router fill:#e8f5e9,stroke:#388e3c,stroke-width:2px,color:#1b5a20;
    classDef domain fill:#fff3e0,stroke:#f57c00,stroke-width:2px,color:#e65100;
    classDef db fill:#ede7f6,stroke:#7e57c2,stroke-width:2px,color:#4a148c;
    classDef proxy fill:#fce4ec,stroke:#d81b60,stroke-width:2px,color:#880e4f;

    Frontend[Frontend Vue.js + Axios]:::client
    Swagger[Swagger UI Docs]:::client

    subgraph AWS_EC2 [AWS EC2 Instance]
        Nginx[Proxy Reverso:<br/>Nginx]:::proxy

        subgraph Docker_Container [Docker Container]
            subgraph Backend_FastAPI [Monolito Modular - FastAPI]
                Main[main.py]
                
                subgraph Infra_DB [Infraestrutura]
                    Engine[engine.py]
                    Session[session.py]
                end

                subgraph Module_Knowledge [Módulo: Knowledge]
                    Router[router.py]:::router
                    DTOs[dtos.py]:::domain
                    Models[models.py]:::domain
                end
            end
        end
    end

    Postgres[(PostgreSQL - AWS RDS)]:::db

    Frontend -->|Chamadas HTTP| Nginx
    Swagger -->|Testes de Endpoints| Nginx
    Nginx -->|Proxy Pass /api/v1| Main
    Main -->|Registra Rotas| Router
    Router -->|Injeta Dependência| Session
    Router -->|Valida Dados| DTOs
    Router -->|Persiste Entidade| Models
    Session --> Engine
    Engine --> Postgres
```

---

## Licença e Objetivo

Este projeto possui caráter exclusivamente acadêmico. Ele foi idealizado e construído como ferramenta prática para o domínio do desenvolvimento Full Stack unindo as tecnologias FastAPI, Vue.js, conteinerização isolada com Docker e deploys automatizados na infraestrutura da AWS usando GitHub Actions.
