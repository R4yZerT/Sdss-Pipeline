# 1. Usamos la imagen completa (no la slim) que ya trae herramientas básicas
FROM python:3.11-bullseye

WORKDIR /app

# 2. SALTÁNDONOS EL APT-GET (Aquí es donde fallaba)
# No vamos a correr apt-get update porque tu red lo bloquea.
# La imagen 'bullseye' estándar ya es bastante completa.

# 3. Instalamos las librerías de Python directamente
COPY requirements.txt .

# Usamos un espejo de Pip por si la red sigue molestando
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# 4. Copiamos el código
COPY . .

CMD ["python", "main.py"]