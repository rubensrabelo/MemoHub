#!/bin/bash
set -e

echo ""
echo "=================================="
echo "Terraform Destroy"
echo "=================================="
echo ""

BASE_DIR=$(pwd)

echo "Entrando na pasta terraform..."
cd "$BASE_DIR/infra/terraform"

echo "Inicializando Terraform..."
terraform init

echo ""
echo "Gerando plano de destruição..."
terraform plan -destroy -out=destroy.tfplan

echo ""
echo "Executando destruição..."
terraform apply destroy.tfplan

echo ""
echo "Removendo arquivos temporários do Terraform..."
rm -f tfplan destroy.tfplan
rm -rf .terraform
rm -f .terraform.lock.hcl
rm -f terraform.tfstate
rm -f terraform.tfstate.backup

echo ""
echo "Removendo arquivos gerados pelo Ansible..."
rm -f "$BASE_DIR/ansible/inventory.yml"
rm -f "$BASE_DIR/ansible/ansible.cfg"

cd "$BASE_DIR"

echo ""
echo "=================================="
echo "Infraestrutura removida"
echo "Ambiente limpo"
echo "=================================="
echo ""
