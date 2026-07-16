# MemoHub - Infrastructure & Configuration Management

> Camada central de infraestrutura, contendo as configurações de proxy reverso local e scripts de provisionamento automatizado em nuvem.

Este diretório centraliza toda a inteligência de DevOps e engenharia de sistemas do **MemoHub**. A estrutura está dividida em duas realidades complementares: o isolamento do ambiente de desenvolvimento local via containers e a orquestração automatizada da topologia de produção multicloud.

---

## Estrutura do Diretório

A árvore de arquivos abaixo detalha a organização dos componentes de configuração de rede e arquivos de automação:

```text
infra/
├── nginx.conf              # Arquivo de configuração de roteamento do Proxy Reverso local
└── terraform/              # Diretório de automação da infraestrutura como código (IaC)
    ├── main.tf             # Orquestrador global e chamada dos módulos técnicos
    ├── providers.tf        # Definição e travas de versão das APIs de nuvem
    ├── variables.tf        # Declaração de tipos de dados das variáveis globais
    ├── outputs.tf          # Exposição de endpoints públicos pós-deploy
    ├── terraform.tfvars    # Arquivo privado contendo os tokens reais de acesso
    ├── README.md           # Guia operacional detalhado do ciclo de vida do Terraform
    └── modules/            # Subpastas de encapsulamento de recursos por plataforma
        ├── neon/           # Módulo de provisionamento do banco PostgreSQL Serverless
        ├── render/         # Módulo de deploy do container Docker da API Python
        └── vercel/         # Módulo de hospedagem edge do cliente web em Vue 3
```

---

## Descrição Detalhada dos Componentes

### 1. Servidor de Proxy Reverso (`nginx.conf`)
O arquivo `nginx.conf` é o cérebro do roteamento de tráfego no ambiente de desenvolvimento local controlado pelo arquivo `docker-compose.dev.yml`. 
* **Objetivo:** Atuar como ponto único de entrada (Edge) na porta padrão HTTP (80).
* **Comportamento:** Intercepta as requisições do usuário no navegador e faz o redirecionamento interno. Chamadas para a raiz `/` são direcionadas para o container do Frontend (Vue 3) e requisições direcionadas para `/api/v1` sofrem um *proxy pass* transparente para o container do Backend (FastAPI), mitigando nativamente qualquer erro de CORS local.

### 2. Orquestração Multicloud (`terraform/`)
A pasta `terraform/` gerencia o ciclo de vida dos recursos de produção na internet de forma declarativa e modular:

* **`main.tf` (Orquestrador Raiz):** Liga os módulos entre si. Captura a string de conexão gerada pelo Neon, aplica o tratamento de dialeto para `postgresql+asyncpg://` e injeta a URL tratada diretamente nas variáveis de ambiente do serviço do Render.
* **`providers.tf` (Plugins):** Registra as assinaturas e travas de versão dos provedores homologados (`kislerdm/neon`, `render-oss/render` e `vercel/vercel`), garantindo que o deploy rode de forma idêntica em qualquer máquina.
* **`modules/neon/`:** Cria o banco de dados isolado no Neon Tech Console e exporta os parâmetros de autenticação criptografados.
* **`modules/render/`:** Configura o serviço de aplicação web no Render no formato `docker`, lendo o `Dockerfile` e gerando o build automático do container Python com `uv`.
* **`modules/vercel/`:** Provisionamento do cliente estático na Vercel, embutindo o objeto `git_repository` para automatizar o build automatizado a cada push na branch principal do GitHub.

---

## Fluxo Operacional de Execução

O ciclo completo de operação desta pasta está segmentado em dois escopos distintos:

### Execução em Desenvolvimento (Local)
O arquivo de proxy do Nginx é montado como um volume de leitura dentro do container do Docker Compose. Nenhuma ação direta é necessária neste diretório para rodar localmente, bastando acionar o comando na raiz:
```bash
docker compose -f docker-compose.dev.yml up --build -d
```

### Execução em Produção (Nuvem)
Para disparar, modificar ou destruir o ambiente estável nas nuvens, navegue até a subpasta do Terraform e utilize os comandos de automação detalhados no guia interno:
```bash
cd terraform/
terraform init
terraform apply -auto-approve
```

Para mais detalhes sobre as variáveis aceitas e como visualizar os links públicos finais gerados após o deploy, consulte o [README detalhado do Terraform](./terraform/README.md).
