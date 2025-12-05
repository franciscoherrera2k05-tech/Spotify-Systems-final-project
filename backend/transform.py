import json
import pandas as pd

def clean_data():
    # Load raw JSON
    with open("raw_spotify.json") as f:
        data = json.load(f)

    df = pd.DataFrame(data)

    # --- VALIDATION RULES ---
    # Remove rows missing required fields
    required = ["id", "name", "artist", "album", "duration_ms", "release_date"]
    df = df.dropna(subset=required)

    # Filter out invalid durations
    df = df[df["duration_ms"].astype(int) > 0]

    # Normalize release_date to year
    df["release_year"] = df["release_date"].str[:4]

    # Keep only valid year values (four digits)
    df = df[df["release_year"].str.match(r"^\d{4}$")]

    # Convert duration to minutes
    df["duration_min"] = df["duration_ms"].astype(int) / 60000

    # Save to cleaned CSV
    df.to_csv("clean_spotify.csv", index=False)
    print(f"Saved clean_spotify.csv with {len(df)} valid rows.")

    return df


if __name__ == "__main__":
    clean_data()