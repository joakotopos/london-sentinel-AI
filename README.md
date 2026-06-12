London Sentinel AI: Motor Prescriptivo de Seguridad Urbana
1. Descripción del Proyecto
Este proyecto consiste en un sistema de Inteligencia Artificial de vanguardia diseñado para procesar datos históricos de criminalidad en Londres mediante el dataset "London Crime". A diferencia de los sistemas de análisis tradicionales, London Sentinel AI implementa una capa prescriptiva que, tras analizar patrones delictivos, genera planes de acción automáticos (como distribución de patrullas y zonas de vigilancia prioritaria) para optimizar la respuesta policial y la prevención del delito en los diversos Boroughs de la capital.

2. Arquitectura Seleccionada
Se ha implementado una arquitectura de Data Lakehouse bajo la metodología Medallion Architecture, la cual organiza los datos en tres etapas de madurez:

Bronze (Raw): Almacenamiento de los datos de criminalidad en su formato original.

Silver (Cleansed): Datos normalizados, con tipos de crímenes estandarizados y limpieza de valores nulos.

Gold (Analytics/AI): Tablas enriquecidas y listas para que el modelo de IA genere predicciones y planes de acción.

El flujo de trabajo utiliza un modelo Híbrido de Gestión, combinando la robustez de una infraestructura Cloud sólida con la agilidad del desarrollo de modelos de Machine Learning.

3. Requisitos y Configuración del Entorno Técnico
Para ejecutar y contribuir en este proyecto, se requieren las siguientes herramientas:

Control de Versiones: Git para el seguimiento de cambios.

Virtualización: Docker y Docker Compose para contenedores.

Lenguaje de Programación: Python 3.10+

Gestión de Base de Datos: PostgreSQL (para metadatos) y Google BigQuery (para consulta y almacenamiento de datos masivos en la nube).

Procesamiento: Apache Spark (PySpark) para procesamiento distribuido de datos.

Modelado de IA: Scikit-learn, XGBoost y MLflow para el seguimiento del ciclo de vida del modelo.

4. Instrucciones de Instalación
Sigue estos pasos para configurar el entorno localmente:

Clonar el repositorio:

Bash
git clone https://github.com/joakotopos/london-sentinel-AI
cd crimes-in-london
Configurar el entorno virtual:

Bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
Instalar dependencias:

Bash
pip install -r requirements.txt
Levantar servicios con Docker:

Bash
docker-compose up -d
Configurar variables de entorno:
Crea un archivo .env en la raíz del proyecto y añade tus credenciales de acceso a la base de datos y llaves de API de Cloud.

INSTRUCCIONES PARA UTILIZAR BIEN LA INGESTA DE DATOS:
1) Cuando usted clone el repositorio, nesesitara ubicar la carpeta raiz del proyecto, en donde debera eliminar la carpeta /.venv si esta carpeta no esta prosiga al paso 2
2) luego de elinar la carpeta, debera ir a la terminar (se recomienda usar la terminal del programa en donde va a ejecutar, para este caso se usara visual studio code), y se ejecutara el siguiendo comando: 
       python -m venv .venv
esto creara la carpeta con el entorno que nesecitara para python
3) debera activar el entorno con el siguiente comando de la terminal:
      .\.venv\Scripts\activate
4) ejecute el siguiente comando para importar y descargar las librerias nesesaarias para la ingesta de datos:
      pip install google-cloud-bigquery pandas db-dtypes pyarrow
5) despues de instalar las librerias, debera elejir el entorno de de python, para esto se apretara la combinacion de teclas ctrl+shif+p, busque la opcion de "select python interpetrer" y seleccione donde esta la carpeta de .venv
6) con estos pasos esta listo para ejecutar el comando python llamada "ingesta_london_crime.py"

INSTRUCCIONES PARA UTILIZAR LA LIMPIEZA DE DATOS
1) al hacer los procesos de ingesta anteriormente, se puede ejecutar el programa "limpieza_london_crime.py"

INSTRUCCIONES PARA CARGAR A SUPABASE (BRONZE + SILVER)
1) Crea un archivo `.env` en la raíz (puedes copiar y editar el archivo `.env.example`). El script lo lee automáticamente:
      - `SUPABASE_URL`: Project URL de Supabase
      - `SUPABASE_KEY`: llave publishable/anon (o usa `SUPABASE_PUBLISHABLE_KEY`)
      - (Opcional) `LONDON_CRIME_LIMIT`: por defecto 50
2) Instala dependencias:
      - `pip install -r requirements.txt`
3) Ejecuta el script one-shot:
      - `python scripts/cargar_a_supabase.py`

Este script inserta:
- `data/bronze/london_test.parquet` -> tabla `london_crime_row`
- `data/processed/london_crime_cleaned.parquet` -> tabla `london_crime_filtered`
5. Estructura del Repositorio
El repositorio está organizado de la siguiente manera para facilitar su navegación:

LONDON-SENTINEL-IA
├── data/               # Diccionarios de datos y muestras de datasets
├── docs/               # Documentación técnica, diagramas y acta de constitución
├── notebooks/          # Jupyter Notebooks para análisis exploratorio (EDA)
├── src/                # Código fuente del proyecto
│   ├── ingestion/      # Scripts de extracción de datos (Capa Bronze)
│   ├── processing/     # Scripts de transformación y limpieza (Capa Silver)
│   ├── models/         # Entrenamiento y lógica de la IA (Capa Gold)
│   └── api/            # Servicio de entrega de planes de acción
├── tests/              # Pruebas unitarias y de integración
├── docker-compose.yml  # Configuración de contenedores
├── requirements.txt    # Lista de dependencias de Python
└── README.md           # Guía general del proyecto



DEFINICION DE PROBLEMAS DE NEGOCIO Y EL PARADIGMA IA  

problema de negocio: la policia de londres y autoridades metropolitanas nesecitan optimizar la distribucion de recursos y patrullaje, para ello, requieren anticipar el volumen de incidentes delictivos que ocurriran en cada comuna segun el periodo de año

paradigmas de aprendizaje: aprendizaje supervisado, ya que contamos con datos historicos etiquetados con el numero real de delitos pasados

tipo de problema: regresion (debido a que la variable que qeremos predecir es un valor numerico continuo: la cantidad de delitos)

variable objetivo: value (numero de incidentes delictivos)

variables predictorias: borought (comuna), major_category (categoria principal del delito), year y month


JUSTIFICACION DE ALGORTIMO
se selecciona el algoritmo de regresion lineal (arbol de desicion) como el modelo base al ser la primera iteracion del ciclo de vida de la IA, se opta por unmodelo de alta interpetabilidad y bajo costo computacional, esto nos permitira establecer una linea de referencia rapida sobre los datos de los cuadrantes de londres sin cart en spbreajuste (overfiting), sirviendo comp punto de comparacion para modelos mas complejos en las siguientes etapas