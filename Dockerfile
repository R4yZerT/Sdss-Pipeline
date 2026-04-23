# 1. Cambiamos a 'bullseye' para evitar el error 403 de los repositorios Trixie
FROM python:3.11-bullseye

# 2. Definimos el directorio de trabajo
WORKDIR /app

# 3. Instalamos dependencias del sistema (usando espejos más estables)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# 4. Copiamos solo los requerimientos primero (para usar la caché de Docker)
COPY requirements.txt .

# 5. Instalamos las librerías de Python para el M4
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# 6. Copiamos el resto de tu código de ML
COPY . .

# 7. Ejecutamos tu script principal
CMD ["python", "main.py"]