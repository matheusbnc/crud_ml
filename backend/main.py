"""Ponto de entrada da aplicação FastAPI.

Este módulo inicializa a aplicação FastAPI, cria as tabelas do banco de dados
e inclui as rotas definidas no roteador principal.
"""

from fastapi import FastAPI
from database import engine
import models
from router import router

# Cria as tabelas do banco de dados, caso não existam.
models.Base.metadata.create_all(bind=engine)

# Instância principal da aplicação FastAPI.
app = FastAPI()

# Inclui as rotas do roteador principal.
app.include_router(router)
