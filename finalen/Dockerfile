# Flask skeleton for Gunnar-botten (see repo FRAMEWORK/README, Phase 2).
# Build rules: one-command-up, self-contained, config via env.
FROM python:3.12-slim

WORKDIR /app

# Install dependencies first for better layer caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Application source
COPY app/ ./app/

# Player fact files live at /srv/players (the tool's base folder).
# The internal trophy code file is written at startup from TROPHY_CODE.
RUN mkdir -p /srv/players && cp -r app/data/players/. /srv/players/

EXPOSE 8101

CMD ["python", "app/main.py"]
