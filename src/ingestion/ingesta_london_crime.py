from google.cloud import bigquery
import os
import pandas as pd

BASE_PATH= os.path.join('data', 'bronze')
os.makedirs(BASE_PATH, exist_ok=True)

file_name= 'london_test.parquet' #nombre especificado para la ingesta de datos
PATH='.../data/bronze'+file_name #donde iran los datos

#esto configura la runa de almacenamiento visual(ingesta cruda)
os.environ['GOOGLE_APPLICATION_CREDENTIALS']=".../planificacion-london-crime-8b30dd3d4499.json" #se agrega el json de las credenciales
cred_path=os.getenv('GOOGLE_APPLICATION_CREDENTIALS')


def ingesta_bigquery_london():
  if not cred_path or not os.path.exists(cred_path):
    print("Archivo de credenciales (.json) no encontrado:", cred_path)
  else:
    client = bigquery.Client()
    
    query= """
            SELECT borough, major_category, minor_category, value, year, month
            FROM `bigquery-public-data.london_crime.crime_by_lsoa`
            LIMIT 10
        """

    df=client.query(query).to_dataframe()
    
    try:
      df.to_parquet(PATH)
      print(f'datos obtenidos exitosamente en {PATH}')
    except Exception as e:
      print(f'directorio no encontrado {PATH}')


if __name__ == "__main__":
    ingesta_bigquery_london()



