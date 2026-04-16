from google.cloud import bigquery
import os

#esto configura la runa de almacenamiento visual(ingesta cruda)
os.makedirs('data/bronze', exist_ok=True)

def ingesta_bigquery_london():
    try:
        client = bigquery.Client()

        query= """
            SELECT borough, major_category, minor_category, value, year, month
            FROM `bigquery-public-data.london_crime.crime_by_lsoa`
            LIMIT 1000
        """

        df=client.query(query).to_dataframe()

        df.to_csv('data/bronze/london_crime_raw.csv', index=False)
        print('ingesta de datos completada') [cite: 13]

    except Exception as e:
        print(f'error de ingesta de datos: {e}') [cite: 20]


if __name__=="__main__":
    ingesta_bigquery_london()