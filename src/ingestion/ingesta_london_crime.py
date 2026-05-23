from google.cloud import bigquery
import os
import pandas as pd

# 1. Configuración de Rutas de Almacenamiento
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
BRONZE_PATH = os.path.join(BASE_DIR, 'data', 'bronze')
os.makedirs(BRONZE_PATH, exist_ok=True) 

FILE_NAME = 'london_test.parquet'
FULL_STORAGE_PATH = os.path.join(BRONZE_PATH, FILE_NAME)

# 2. Configuración de Credenciales
JSON_NAME = "planificacion-london-crime-777f76970c1b.json"
DIRECTORIO_SCRIPT = os.path.dirname(os.path.abspath(__file__))
RUTA_JSON = os.path.join(DIRECTORIO_SCRIPT, JSON_NAME)

print(f"Archivos encontrados en la carpeta: {os.listdir(DIRECTORIO_SCRIPT)}")

# Si ya existe GOOGLE_APPLICATION_CREDENTIALS, se respeta.
# Si no existe, se usa el JSON local (si está presente en la carpeta del script).
if not os.getenv("GOOGLE_APPLICATION_CREDENTIALS") and os.path.exists(RUTA_JSON):
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = RUTA_JSON

# Límite de filas para evitar demoras (configurable con la variable de entorno LONDON_CRIME_LIMIT)
DEFAULT_LIMIT = int(os.getenv("LONDON_CRIME_LIMIT", "50"))

def ingesta_bigquery_london(limit: int = DEFAULT_LIMIT):
    credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    if credentials_path and not os.path.exists(credentials_path):
        print(
            f"\nERROR CRÍTICO: GOOGLE_APPLICATION_CREDENTIALS apunta a un archivo inexistente: {credentials_path}"
        )
        return

    if not credentials_path and not os.path.exists(RUTA_JSON):
        print(
            "\nERROR CRÍTICO: No se encontraron credenciales para BigQuery. "
            f"Agrega el JSON en: {RUTA_JSON} o define GOOGLE_APPLICATION_CREDENTIALS."
        )
        return

    if limit is None:
        limit = DEFAULT_LIMIT

    try:
        limit = int(limit)
    except (TypeError, ValueError):
        print(f"\nERROR: El parámetro 'limit' debe ser un entero. Valor recibido: {limit}")
        return

    if limit <= 0:
        print(f"\nERROR: El parámetro 'limit' debe ser mayor a 0. Valor recibido: {limit}")
        return

    try:
        client = bigquery.Client()
        query = f"""
           SELECT borough, major_category, minor_category, value, year, month
    FROM `bigquery-public-data.london_crime.crime_by_lsoa`
    WHERE year >= 2011
    LIMIT {limit}
        """
        df = client.query(query).to_dataframe()
        df.to_parquet(FULL_STORAGE_PATH, index=False)
        print(f'\n¡ÉXITO! Datos guardados en {FULL_STORAGE_PATH}')

    except Exception as e:
        print(f'\nError técnico durante la ingesta: {e}')

if __name__ == "__main__":
    ingesta_bigquery_london()
