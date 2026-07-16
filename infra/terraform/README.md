# Terraform

Aqui estão os blocos de comandos completamente separados e comentados para você gerenciar o ciclo de vida da sua infraestrutura sem nenhuma confusão.
Certifique-se de estar dentro da pasta infra/terraform/ no seu terminal antes de executar qualquer um deles.
------------------------------
## 🚀 1. COMANDOS PARA SUBIR (Criar toda a infraestrutura)
Use esta sequência quando quiser limpar os caches antigos locais, ler os arquivos corrigidos e fazer o deploy do zero do Neon DB, Render e Vercel:

```bash
# Apaga caches de provedores e planos antigos que falharam
rm -rf .terraform .terraform.lock.hcl terraform.tfstate terraform.tfstate.backup
# Inicializa o ambiente do zero e baixa os plugins corretos
terraform init
# Valida a sintaxe e desenha o plano de criação
terraform plan
# Executa o deploy integrado e cria tudo conectado de forma automática
terraform apply -auto-approve
```

------------------------------
## 🗑️ 2. COMANDOS PARA DESTRUIR (Apagar tudo das nuvens)
Use esta sequência quando quiser remover completamente todos os recursos criados de dentro das plataformas (Neon, Render e Vercel) para não queimar os limites das suas contas gratuitas, além de limpar o seu computador:

```bash
# Deleta de forma limpa e automática o banco, a API e o Front do ar
terraform destroy -auto-approve
# Remove todos os arquivos locais de estado gerados pelo Terraform
rm -rf .terraform .terraform.lock.hcl terraform.tfstate terraform.tfstate.backup
```

------------------------------
## 🔒 Passo Final no Git (Após o sucesso do deploy)
Assim que você rodar os comandos para subir e o terminal exibir as mensagens de sucesso em verde, mude para a pasta raiz do monorepo (cd ../..) e salve o código final na sua branch:

git add .
git commit -m "feat(infra): orchestrate serverless PaaS ecosystem using modular Terraform for Neon, Render, and Vercel"
git push origin feat/terraform-paas

Salvando o arquivo do Render com o cifrão e rodando o bloco de comandos para subir, o Terraform concluiu a criação de tudo com sucesso?

