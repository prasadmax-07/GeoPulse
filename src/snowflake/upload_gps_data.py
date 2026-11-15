
import os
import pandas as pd
import snowflake.connector

from pathlib import Path
from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parents[2]
load_dotenv(PROJECT_ROOT / ".env")

CSV_FILE = PROJECT_ROOT / "data" / "synthetic" / "gps_mobility_data.csv"

def upload_gps_data():

    connection = None
    cursor = None

    try:
        print("Reading GPS dataset...")

        df = pd.read_csv(CSV_FILE)

        print("Rows loaded:", len(df))
        print("Columns:", list(df.columns))

        connection = snowflake.connector.connect(
            account=os.getenv("SNOWFLAKE_ACCOUNT"),
            user=os.getenv("SNOWFLAKE_USER"),
            authenticator="PROGRAMMATIC_ACCESS_TOKEN",
            token=os.getenv("SNOWFLAKE_TOKEN"),
            warehouse=os.getenv("SNOWFLAKE_WAREHOUSE"),
            database=os.getenv("SNOWFLAKE_DATABASE"),
            schema=os.getenv("SNOWFLAKE_SCHEMA"),
            role=os.getenv("SNOWFLAKE_ROLE")
        )

        cursor = connection.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS GPS_MOBILITY_DATA (
                DEVICEID VARCHAR(100),
                LATITUDE FLOAT,
                LONGITUDE FLOAT,
                TIMESTAMP TIMESTAMP_NTZ,
                LOCATIONZONE VARCHAR(100)
            )
        """)

        print("Snowflake table ready.")

        cursor.execute("TRUNCATE TABLE GPS_MOBILITY_DATA")

        insert_query = """
            INSERT INTO GPS_MOBILITY_DATA
            (DEVICEID, LATITUDE, LONGITUDE, TIMESTAMP, LOCATIONZONE)
            VALUES (%s, %s, %s, %s, %s)
        """

        records = list(df.itertuples(index=False, name=None))

        cursor.executemany(insert_query, records)

        cursor.execute("SELECT COUNT(*) FROM GPS_MOBILITY_DATA")
        count = cursor.fetchone()[0]

        print("\n========== UPLOAD REPORT ==========")
        print("CSV rows:", len(df))
        print("Snowflake rows:", count)

        if count == len(df):
            print("GPS dataset uploaded successfully!")
        else:
            print("WARNING: Row counts do not match.")

    except Exception as error:
        print("Upload failed:", error)

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
            print("Snowflake connection closed.")


if __name__ == "__main__":
    upload_gps_data()
