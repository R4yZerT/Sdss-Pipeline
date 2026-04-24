# Usamos la imagen completa y estable, compatible con ARM64 (M4)
FROM python:3.11-bullseye

# Directorio de trabajo
WORKDIR /app

# Copiamos primero los requerimientos
COPY requirements.txt .

# Instalamos todo sin caché para evitar basuras previas
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copiamos TODOS los archivos del repo al contenedor (incluido data/sdss_sample.csv)
COPY . .

# Comando de ejecución
CMD ["python", "main.py"]