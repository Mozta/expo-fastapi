# Imagen base: Python 3.12 - versión ligera (Debian)
FROM python:3.12-slim

# No generar .pyc y mostrarf los logs al instante
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONBUFFERED=1

# Carpera de trabajo dentro del contedor
WORKDIR /code

# Copya e instala las dependencias 
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código fuente
COPY app ./app

# Puerto en el que escucha la API dentro del contenedor
EXPOSE 8000

# fastapi run escuche 0.0.0.0 (y no en 127.0.0.1)
CMD ["fastapi", "run", "app/main.py", "--port", "8000"]