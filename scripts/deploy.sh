#!/bin/bash
set -e

echo ""
echo "=================================="
echo "Terraform Deploy"
echo "=================================="
echo ""

BASE_DIR=$(pwd)

echo "Entrando na pasta terraform..."
cd "$BASE_DIR/infra/terraform"

echo ""
echo "Inicializando Terraform..."
terraform init

echo ""
echo "Formatando arquivos..."
terraform fmt -recursive

echo ""
echo "Validando configuração..."
terraform validate

echo ""
echo "Gerando plano..."
terraform plan -out=tfplan

echo ""
echo "Aplicando infraestrutura..."
terraform apply tfplan

echo ""
echo "Obtendo outputs..."
BACKEND=$(terraform output -raw render_backend_url)
FRONTEND=$(terraform output -raw vercel_frontend_url)

echo ""
echo "----------------------------------"
echo "URLS DA INFRAESTRUTURA:"
echo "BACKEND:  $BACKEND/docs"
echo "FRONTEND: $FRONTEND"
echo "----------------------------------"

cd "$BASE_DIR"

echo ""
echo "=================================="
echo "Deploy concluído com sucesso!"
echo "=================================="
echo ""
