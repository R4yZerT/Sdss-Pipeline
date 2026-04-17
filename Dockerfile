# ── Base ──────────────────────────────────────────────────────────────────────
FROM python:3.11-slim

# Metadatos
LABEL maintainer="Big Data IUE"
LABEL description="SDSS ML Pipeline — Clasificación, Regresión y Clustering"

# ── Variables de entorno ───────────────────────────────────────────────────────
ENV DATA_PATH=/app/data/sdss_sample.csv
ENV OUTPUT_DIR=/app/outputs
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# ── Directorio de trabajo ──────────────────────────────────────────────────────
WORKDIR /app

# ── Dependencias del sistema ───────────────────────────────────────────────────
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# ── Dependencias Python ────────────────────────────────────────────────────────
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ── Código fuente ──────────────────────────────────────────────────────────────
COPY src/ ./src/
COPY tests/ ./tests/
COPY main.py .

# ── Carpeta de datos (se monta como volumen o se copia) ───────────────────────
RUN mkdir -p /app/data /app/outputs

# ── Punto de entrada ───────────────────────────────────────────────────────────
CMD ["python", "main.py"]
