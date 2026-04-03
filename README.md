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


###NOTA####
por el momento todo es teorico y puede cambiar por el tiempo a medida de como avance la estructura del proyecto