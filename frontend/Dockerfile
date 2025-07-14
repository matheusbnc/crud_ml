# Use imagem oficial Python slim para frontend Streamlit
FROM python:3.11-slim

# Define o diretório da aplicação
WORKDIR /app

# Copia arquivos do frontend para dentro do container
COPY . /app

# Instala dependências (ajuste se precisar de mais libs)
RUN pip install --no-cache-dir streamlit requests pandas

# Expõe a porta padrão do Streamlit
EXPOSE 8501

# Comando para rodar o app Streamlit no container
CMD ["streamlit", "run", "streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0"]
