import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

def load_sql():
    load_dotenv()

    df = pd.read_csv("clean_spotify.csv")

    # Use DATABASE_URL from environment
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        raise ValueError("DATABASE_URL not found in environment variables")

    engine = create_engine(database_url)

    df.to_sql("tracks", engine, if_exists="replace", index=False)
    print("Loaded into PostgreSQL.")

if __name__ == "__main__":
    load_sql()