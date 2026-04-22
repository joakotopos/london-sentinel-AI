import pandas as pd
import os

#aqui se definen las rutas 
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PATH_RAW = os.path.join(BASE_DIR, 'data', 'bronze', 'london_test.parquet')
PATH_PROCESSED = os.path.join(BASE_DIR, 'data', 'processed')
os.makedirs(PATH_PROCESSED, exist_ok=True)

#limpieza de datos
def limpieza_datos():
    try:
        #cargar datos
        df= pd.read_parquet(PATH_RAW)
        print(f"datos cargados, registros iniciales: {len(df)}")

        #eliminar duplicados
        df = df.drop_duplicates()
        print(f"datos después de eliminar duplicados: {len(df)}")

        #estandarizar nombres de columnas
        # primero convertir a minúsculas
        df['major_category'] = df['major_category'].str.lower()
        df['minor_category'] = df['minor_category'].str.lower()

        # transformacion a columnas derivadas
        #crear una columna de fecha simple para analisis posterior
        df['periodo']= df['year'].astype(str) + '-' + df['month'].astype(str).str.zfill(2)

        #guardar datos limpios
        output_file = os.path.join(PATH_PROCESSED, 'london_crime_cleaned.parquet')
        df.to_parquet(output_file, index=False)

        print(f"¡Limpieza exitosa! Datos guardados en: {output_file}")
        print(f"Registros finales después de limpieza: {len(df)}")

    except Exception as e:
        print(f"Error durante la limpieza de datos: {e}")

if __name__ == "__main__":    limpieza_datos()