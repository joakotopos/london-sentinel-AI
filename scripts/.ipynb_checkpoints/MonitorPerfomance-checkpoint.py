import time
import os
import psutil
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LinearRegression

# 1. Resolver las rutas de forma dinámica según la ubicación del script
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, 'data', 'processed', 'london_crime_cleaned.parquet')

# 2. Capturar estado INICIAL del sistema
process = psutil.Process(os.getpid())
ram_inicial = process.memory_info().rss / (1024 * 1024)  # MB
cpu_inicial = psutil.cpu_percent(interval=None)
tiempo_inicial = time.time()

print("=== Iniciando Monitoreo Técnico del Pipeline ===")

#EJECUCIÓN COMPLETA DEL PIPELINE
df = pd.read_parquet(DATA_PATH, engine='fastparquet')

X = df[['borough', 'major_category', 'year', 'month']]
y_log = np.log1p(df['value'])

# Procesamiento (Transformación)
preprocessor = ColumnTransformer(
    transformers=[
        ('cat', OneHotEncoder(drop='first', sparse_output=False), ['borough', 'major_category'])
    ],
    remainder='passthrough'
)
X_processed = preprocessor.fit_transform(X)

# División
X_train, X_test, y_train, y_test = train_test_split(
    X_processed, y_log, test_size=0.2, random_state=42
)

# Entrenamiento
model_log = LinearRegression()
model_log.fit(X_train, y_train)
# ==========================================================

# 4. Capturar estado FINAL del sistema
tiempo_final = time.time()
ram_final = process.memory_info().rss / (1024 * 1024)  # MB
cpu_final = psutil.cpu_percent(interval=None)

# 5. Calcular métricas netas
tiempo_total = tiempo_final - tiempo_inicial
ram_consumida_neta = max(0, ram_final - ram_inicial)
uso_cpu_promedio = abs(cpu_final - cpu_inicial)

# 6. Mostrar datos exactos en consola
print("\n=====================================================")
print("   MÉTRICAS EXACTAS PARA TU TABLA DE RENDIMIENTO")
print("=====================================================")
print(f"Tiempo total de ejecución : {tiempo_total:.4f} segundos")
print(f"Consumo neto de Memoria RAM: {ram_consumida_neta:.2f} MB")
print(f"Carga estimada de CPU      : {uso_cpu_promedio:.1f} %")
print("=====================================================")