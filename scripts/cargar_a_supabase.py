import os
import sys
from datetime import datetime, timezone

import pandas as pd
from supabase import create_client


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)

from src.ingestion.ingesta_london_crime import ingesta_bigquery_london  # noqa: E402
from src.processing.limpieza_london_crime import limpieza_datos  # noqa: E402

BRONZE_PARQUET_PATH = os.path.join(BASE_DIR, "data", "bronze", "london_test.parquet")
SILVER_PARQUET_PATH = os.path.join(BASE_DIR, "data", "processed", "london_crime_cleaned.parquet")


def _load_dotenv(dotenv_path: str) -> None:
    if not os.path.exists(dotenv_path):
        return

    try:
        with open(dotenv_path, "r", encoding="utf-8") as f:
            for raw_line in f:
                line = raw_line.strip()
                if not line or line.startswith("#"):
                    continue
                if "=" not in line:
                    continue

                key, value = line.split("=", 1)
                key = key.strip()
                value = value.strip().strip('"').strip("'")

                if key:
                    os.environ.setdefault(key, value)
    except OSError:
        # Si el archivo no se puede leer, seguimos y dejamos que falle más adelante con un mensaje claro.
        return


def _df_to_records(df: pd.DataFrame) -> list[dict]:
    df = df.where(pd.notnull(df), None)
    records = df.to_dict(orient="records")

    normalized: list[dict] = []
    for row in records:
        clean_row: dict = {}
        for key, value in row.items():
            if hasattr(value, "item"):
                value = value.item()
            clean_row[key] = value
        normalized.append(clean_row)

    return normalized


def _batch(records: list[dict], batch_size: int) -> list[list[dict]]:
    return [records[i : i + batch_size] for i in range(0, len(records), batch_size)]


def _insert_in_batches(supabase, table_name: str, records: list[dict], batch_size: int = 100) -> None:
    if not records:
        print(f"No hay registros para insertar en '{table_name}'.")
        return

    batches = _batch(records, batch_size)
    for idx, batch in enumerate(batches, start=1):
        supabase.table(table_name).insert(batch).execute()
        print(f"Insertado batch {idx}/{len(batches)} en '{table_name}' (rows={len(batch)}).")


def main() -> None:
    _load_dotenv(os.path.join(BASE_DIR, ".env"))

    supabase_url = os.getenv("SUPABASE_URL")
    supabase_key = os.getenv("SUPABASE_KEY") or os.getenv("SUPABASE_PUBLISHABLE_KEY")

    if not supabase_url or not supabase_key:
        raise SystemExit(
            "Faltan variables de entorno. Define SUPABASE_URL y SUPABASE_KEY (o SUPABASE_PUBLISHABLE_KEY)."
        )

    limit = int(os.getenv("LONDON_CRIME_LIMIT", "50"))
    timestamp = datetime.now(timezone.utc).isoformat()

    print(f"Ejecutando ingesta desde BigQuery (limit={limit})...")
    ok = ingesta_bigquery_london(limit=limit)
    if not ok:
        raise SystemExit(
            "La ingesta desde BigQuery falló (credenciales o consulta). "
            "No se continuará para evitar cargar datos antiguos a Supabase."
        )

    if not os.path.exists(BRONZE_PARQUET_PATH):
        raise SystemExit(
            f"No se encontró el archivo bronze esperado en: {BRONZE_PARQUET_PATH}. "
            "Verifica que la ingesta haya terminado correctamente."
        )

    df_bronze = pd.read_parquet(BRONZE_PARQUET_PATH)
    df_bronze["ingested_at"] = timestamp
    bronze_records = _df_to_records(df_bronze)

    print("Conectando a Supabase e insertando tabla london_crime_row...")
    supabase = create_client(supabase_url, supabase_key)
    _insert_in_batches(supabase, "london_crime_row", bronze_records, batch_size=100)

    print("Ejecutando limpieza (silver) y generando dataset filtrado...")
    limpieza_datos()

    if not os.path.exists(SILVER_PARQUET_PATH):
        raise SystemExit(
            f"No se encontró el archivo silver esperado en: {SILVER_PARQUET_PATH}. "
            "Verifica que la limpieza haya terminado correctamente."
        )

    df_silver = pd.read_parquet(SILVER_PARQUET_PATH)
    df_silver["cleaned_at"] = timestamp
    silver_records = _df_to_records(df_silver)

    print("Insertando tabla london_crime_filtered...")
    _insert_in_batches(supabase, "london_crime_filtered", silver_records, batch_size=100)

    print("Listo: bronze -> london_crime_row, silver -> london_crime_filtered")


if __name__ == "__main__":
    main()
