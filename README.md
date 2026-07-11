# MemoHub

> Sua base pessoal de conhecimento.

O **MemoHub** é uma aplicação web para armazenar perguntas e respostas sobre qualquer assunto. A ideia é centralizar informações importantes em um único lugar, permitindo consultar rapidamente dúvidas resolvidas sem precisar pesquisar novamente.

Diferente de um aplicativo de notas tradicional, o MemoHub é organizado no formato **Pergunta → Resposta**, tornando o conhecimento mais fácil de localizar e reutilizar.

## Funcionalidades

* Cadastro de perguntas e respostas.
* Edição de registros.
* Exclusão de registros.
* Pesquisa por título ou pergunta.
* Organização por categoria.
* Marcação de favoritos.
* Ordenação por data de criação.

## Exemplo

**Título**

> Como criar uma API com FastAPI?

**Categoria**

> Programação

**Pergunta**

> Como criar uma rota GET utilizando FastAPI?

**Resposta**

> Utilize o decorador `@app.get()` para definir uma rota que responda às requisições HTTP GET.

---

**Título**

> Como cozinhar arroz?

**Categoria**

> Culinária

**Pergunta**

> Qual a proporção entre arroz e água?

**Resposta**

> Geralmente utiliza-se uma medida de arroz para duas medidas de água.

## Tecnologias

### Backend

* Python
* FastAPI
* SQLAlchemy
* PostgreSQL

### Frontend

* Vue.js
* Axios
* Vue Router

### Infraestrutura

* Docker
* Docker Compose
* AWS EC2
* AWS RDS PostgreSQL
* GitHub Actions (CI/CD)

## Arquitetura

```
Vue.js
    │
 Axios
    │
FastAPI
    │
SQLAlchemy
    │
PostgreSQL (AWS RDS)
```

## Modelo de Dados

A aplicação utiliza apenas uma entidade principal.

| Campo     | Tipo     | Descrição                  |
| --------- | -------- | -------------------------- |
| id        | Long     | Identificador              |
| title     | String   | Título da dúvida           |
| question  | String   | Pergunta                   |
| answer    | String   | Resposta                   |
| category  | String   | Categoria                  |
| favorite  | Boolean  | Indica se é favorita       |
| createdAt | DateTime | Data de criação            |
| updatedAt | DateTime | Data da última atualização |

## Objetivo

O objetivo deste projeto é servir como uma base de conhecimento pessoal, permitindo registrar e consultar informações sobre qualquer tema, como:

* Programação
* Banco de Dados
* Redes
* Cloud Computing
* Faculdade
* Trabalho
* Idiomas
* Culinária
* Finanças
* Saúde
* Hobbies
* Qualquer outro assunto de interesse

## API REST

| Método | Endpoint        | Descrição                |
| ------ | --------------- | ------------------------ |
| GET    | /knowledge      | Lista todos os registros |
| GET    | /knowledge/{id} | Busca um registro        |
| POST   | /knowledge      | Cria um registro         |
| PUT    | /knowledge/{id} | Atualiza um registro     |
| DELETE | /knowledge/{id} | Remove um registro       |

## Funcionalidades Futuras

* Upload de imagens.
* Suporte a Markdown.
* Busca por palavras-chave.
* Sistema de tags.
* Exportação para PDF.
* Compartilhamento de registros.
* Login de usuários.
* Integração com IA para sugerir respostas relacionadas.

## Licença

Este projeto foi desenvolvido para fins acadêmicos, como prática de desenvolvimento Full Stack utilizando FastAPI, Vue.js, Docker, PostgreSQL, AWS e GitHub Actions.
