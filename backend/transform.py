import json
import pandas as pd

def clean_data():
  with open("raw_spotify.json") as f:
      data = json.load(f)

  df = pd.DataFrame(data)

  df["duration_min"] = df["duration_ms"] / 60000
  df["release_year"] = df["release_date"].str[:4]

  df.to_csv("clean_spotify.csv", index=False)
  print("Saved clean_spotify.csv")
  return df

if __name__ == "__main__":
  clean_data()
