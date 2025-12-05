import spotipy
import json

def extract_tracks(access_token):
    sp = spotipy.Spotify(auth=access_token)

    results = sp.current_user_top_tracks(limit=20, time_range="short_term")
    items = results["items"]

    data = []
    for t in items:
        data.append({
            "id": t["id"],
            "name": t["name"],
            "artist": ", ".join([a["name"] for a in t["artists"]]),
            "album": t["album"]["name"],
            "popularity": t["popularity"],
            "duration_ms": t["duration_ms"],
            "release_date": t["album"]["release_date"]
        })

    with open("raw_spotify.json", "w") as f:
        json.dump(data, f, indent=4)

    print("Saved raw_spotify.json")
