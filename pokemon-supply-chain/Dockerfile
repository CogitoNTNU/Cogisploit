FROM python:3.15-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app.py .
COPY pokedex.json .
COPY templates templates
COPY static static
EXPOSE 8101 8102
CMD ["python", "app.py"]
