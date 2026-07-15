# Camada 1: Construtor (Builder)
FROM node:20-alpine AS builder

WORKDIR /app

COPY package*.json ./

RUN npm ci

COPY . .

ARG VITE_API_URL
ENV VITE_API_URL=$VITE_API_URL

RUN npm run build

# --- TRANSICAO: ESTAGIO DE EXECUCAO ---
FROM alpine:latest
WORKDIR /app
COPY --from=builder /app/dist /app/dist
CMD ["tail", "-f", "/dev/null"]
