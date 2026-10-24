FROM python:3.10-slim

WORKDIR /app

# Installation des dépendances système de base
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copie et installation des dépendances Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copie du code du serveur
COPY server.py .

# Commande de lancement dynamique pour Render
CMD uvicorn server:app --host 0.0.0.0 --port ${PORT:-10000}
