# CRUD com Streamlit + FastAPI + PostgreSQL

Este projeto demonstra a criação de uma aplicação CRUD simples integrando **Streamlit** (frontend), **FastAPI** (backend) e **PostgreSQL** (banco de dados relacional), ideal para fins de aprendizado e portfólio. O objetivo é ilustrar como construir uma aplicação fullstack leve com foco em organização de código, comunicação entre serviços e persistência de dados.

## 🧩 Tecnologias Utilizadas

- [FastAPI](https://fastapi.tiangolo.com/) — API backend rápida e moderna  
- [Streamlit](https://streamlit.io/) — Interface web interativa  
- [PostgreSQL](https://www.postgresql.org/) — Banco de dados relacional  
- [SQLAlchemy](https://www.sqlalchemy.org/) — ORM para manipulação do banco  
- [Docker](https://www.docker.com/) — Containerização dos serviços  

## 📁 Estrutura do Projeto

```
crud_ml/
├── backend/
│   ├── Dockerfile          # Dockerfile do backend
│   ├── main.py             # Entry point da API FastAPI
│   ├── database.py         # Conexão com o banco de dados
│   ├── models.py           # Modelos SQLAlchemy
│   ├── crud.py             # Funções CRUD para produtos
│   ├── router.py           # Rotas FastAPI
│   ├── schema.py           # Schemas Pydantic
│   └── requirements.txt    # Dependências Python do backend
├── frontend/
│   ├── app.py              # Interface em Streamlit
│   └── Dockerfile          # Dockerfile do frontend
│   └── requirements.txt    # Dependências Python do frontend
├── docker-compose.yml      # Orquestração dos serviços
└── README.md               # Documentação do projeto
```


## 🚀 Como Executar Localmente

### Pré-requisitos

- Docker e Docker Compose instalados

### Passo a passo

```bash
# Clone o repositório
git clone https://github.com/matheusbnc/crud_ml.git
cd crud_ml

# Suba os containers
docker-compose up --build
```

Acesse:

- Frontend: `http://localhost:8501`  
- API FastAPI: `http://localhost:8000/docs`

> Obs: O banco de dados será criado automaticamente via Docker.

## 📦 Funcionalidades

- 🔍 Listar produtos  
- ➕ Adicionar novos produtos  
- ✏️ Editar produtos existentes  
- ❌ Remover produtos  

## 🛠️ Melhorias Futuras

- Autenticação de usuários  
- Testes automatizados  
- Upload de imagens  
- Deploy em ambiente cloud  

## 💡 Objetivo

Este projeto foi desenvolvido como parte do meu portfólio para demonstrar habilidades em desenvolvimento fullstack com Python, Docker, APIs REST e integração entre serviços.

## 🧑‍💻 Autor

**Matheus Barros**  
[LinkedIn](https://www.linkedin.com/in/matheusbnc/)  
[GitHub](https://github.com/matheusbnc)

---

⭐ Se você gostou do projeto, deixe uma estrela no repositório!
