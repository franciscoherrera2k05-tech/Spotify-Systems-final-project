import os
import pandas as pd

def test_clean_csv_exists():
    assert os.path.exists("backend/clean_spotify.csv"), "Clean CSV not found"

def test_columns():
    df = pd.read_csv("backend/clean_spotify.csv")
    expected_columns = ["name", "artist", "album", "popularity", "duration_ms", "release_date", "duration_min", "release_year"]
    assert all(col in df.columns for col in expected_columns), "Columns missing in CSV"

if __name__ == "__main__":
    try:
        test_clean_csv_exists()
        test_columns()
        print("All tests passed")
    except AssertionError as e:
        print("Test failed:", e)
