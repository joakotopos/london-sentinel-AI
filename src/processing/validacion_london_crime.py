import pandas as pd
import os

# Configuración de rutas
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PATH_PROCESSED = os.path.join(BASE_DIR, 'data', 'processed', 'london_crime_cleaned.parquet')
PATH_REPORTS = os.path.join(BASE_DIR, 'data', 'reports')
os.makedirs(PATH_REPORTS, exist_ok=True)

def validar_datos():
    try:
        df = pd.read_parquet(PATH_PROCESSED)
        errores = []

        #Validación Estructural: Columnas obligatorias
        cols_requeridas = ['borough', 'major_category', 'value', 'year', 'month']
        for col in cols_requeridas:
            if col not in df.columns:
                errores.append(f"Falta columna obligatoria: {col}")

        #Validación Semántica: Valores negativos
        if (df['value'] < 0).any():
            num_negativos = (df['value'] < 0).sum()
            errores.append(f"Se encontraron {num_negativos} registros con valores negativos en 'value'")

        #Validación Semántica: Rango de años (Ejemplo: 2008-2026)
        if not df['year'].between(2008, 2026).all():
            errores.append("Existen registros con años fuera del rango esperado")

        #Generación de Reporte
        report_path = os.path.join(PATH_REPORTS, 'reporte_errores.txt')
        with open(report_path, 'w') as f:
            if not errores:
                f.write("Validación exitosa: No se detectaron errores estructurales ni semánticos.")
                print("Validación completada sin errores.")
            else:
                f.write("ERRORES DETECTADOS EN EL DATASET:\n")
                for error in errores:
                    f.write(f"- {error}\n")
                print(f"Validación finalizada. Se detectaron {len(errores)} errores. Ver reporte en {report_path}")

    except Exception as e:
        print(f"Error durante el proceso de validación: {e}")

if __name__ == "__main__":
    validar_datos()