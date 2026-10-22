# BRAIN Hovedkvarter — challenge-appen.
# Byggeregler (FRAMEWORK.md, fase 2): én kommando opp, selvforsynt, konfig via env.
FROM python:3.12-slim

WORKDIR /app

# Installer avhengigheter først for bedre layer-caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Applikasjonskilde
COPY app/ ./app/

EXPOSE 8000

CMD ["python", "app/main.py"]
