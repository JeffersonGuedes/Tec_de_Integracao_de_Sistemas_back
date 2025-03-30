FROM python:3.11-slim

# Atualiza pacotes e instala dependências necessárias
RUN apt-get update && apt-get install -y \
    libpq-dev gcc \
    dos2unix \
    && rm -rf /var/lib/apt/lists/*

# Cria um grupo e usuário não-root chamado "celery"
RUN groupadd -r celery && useradd -r -g celery celery

# Define variáveis de ambiente
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app

# Define o diretório de trabalho
WORKDIR /app

# Copia e instala as dependências
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia o código da aplicação
COPY . .

# Cria diretórios para logs e estado do Celery e define permissões
RUN mkdir -p /var/log/celery /var/run/celery && \
    chown -R celery:celery /var/log/celery /var/run/celery

# Copia e ajusta permissões do script de inicialização
COPY start.sh /start.sh
RUN dos2unix /start.sh && \
    chmod +x /start.sh

# Expõe a porta do Gunicorn
EXPOSE 8000

# Define o comando de inicialização
CMD ["sh", "/start.sh"]
