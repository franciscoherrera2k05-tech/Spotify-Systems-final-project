import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

def load_sql():
    load_dotenv()

    df = pd.read_csv("clean_spotify.csv")

    db_user = os.getenv("POSTGRES_USER")
    db_password = os.getenv("POSTGRES_PASSWORD")
    db_name = os.getenv("POSTGRES_DB", "spotifydb")

    database_url = f"postgresql://{db_user}:{db_password}@postgres:5432/{db_name}"

    engine = create_engine(database_url)

    df.to_sql("tracks", engine, if_exists="replace", index=False)
    print("Loaded into PostgreSQL.")

if __name__ == "__main__":
    load_sql()