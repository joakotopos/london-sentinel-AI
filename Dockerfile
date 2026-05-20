# 1. Imagen base ligera de Python
FROM python:3.11-slim

# 2. Evita archivos temporales y muestra errores en tiempo real
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# 3. Directorio de trabajo dentro del contenedor
WORKDIR /app

# 4. Instalar herramientas del sistema necesarias para compilar librerías de datos
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# 5. Copiar e instalar las librerías del proyecto (pandas, pyarrow, bigquery, etc.)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 6. Copiar todo el código del proyecto al contenedor
COPY . .

CMD ["python"]