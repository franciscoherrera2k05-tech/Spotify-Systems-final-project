import pandas as pd
from sqlalchemy import create_engine
import os

def load_sql(df, user_id):
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        raise ValueError("DATABASE_URL not found in environment variables")

    engine = create_engine(database_url)
    table_name = f"tracks_{user_id}"  # each user gets a separate table

    df.to_sql(table_name, engine, if_exists="replace", index=False)
    print(f"Loaded tracks into table {table_name}.")

# Optional CLI
if __name__ == "__main__":
    import sys
    import transform
    df = transform.clean_data()
    load_sql(df, user_id="testuser")

