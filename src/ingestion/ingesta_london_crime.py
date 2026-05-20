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

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = RUTA_JSON

def ingesta_bigquery_london():
    if not os.path.exists(RUTA_JSON):
        print(f"\nERROR CRÍTICO: El archivo NO existe en: {RUTA_JSON}")
        return

    try:
        client = bigquery.Client()
        query = """
           SELECT borough, major_category, minor_category, value, year, month
    FROM `bigquery-public-data.london_crime.crime_by_lsoa`
    WHERE year >= 2011
        """
        df = client.query(query).to_dataframe()
        df.to_parquet(FULL_STORAGE_PATH, index=False)
        print(f'\n¡ÉXITO! Datos guardados en {FULL_STORAGE_PATH}')

    except Exception as e:
        print(f'\nError técnico durante la ingesta: {e}')

if __name__ == "__main__":
    ingesta_bigquery_london()
