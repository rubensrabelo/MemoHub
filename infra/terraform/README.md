# Terraform

```bash
meu-projeto/
└── terraform/
    ├── modules/
    │   ├── neon/
    │   │   ├── main.tf
    │   │   ├── outputs.tf
    │   │   └── variables.tf
    │   ├── render/
    │   │   ├── main.tf
    │   │   ├── outputs.tf
    │   │   └── variables.tf
    │   └── vercel/
    │       ├── main.tf
    │       └── variables.tf
    ├── main.tf          # Orquestrador (chama os módulos)
    ├── providers.tf     # Configuração global dos provedores
    ├── variables.tf     # Variáveis globais (API Keys)
    └── terraform.tfvars # Seus tokens reais (NUNCA envie ao Git)

```