from flask import Flask, redirect, request, url_for, render_template, session
from flask_cors import CORS
import pandas as pd
from sqlalchemy import create_engine
from extract_spotify import extract_tracks
from transform import clean_data
from load_sql import load_sql
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET", "replace_with_secret")
CORS(app)

# Spotify OAuth (no static cache file)
auth_manager = SpotifyOAuth(
    client_id=os.getenv("SPOTIPY_CLIENT_ID"),
    client_secret=os.getenv("SPOTIPY_CLIENT_SECRET"),
    redirect_uri=os.getenv("REDIRECT_URL"),
    scope="user-top-read",
    cache_path=None  # important: disables static cache
)

# Database connection
database_url = os.getenv("DATABASE_URL")
if not database_url:
    raise ValueError("DATABASE_URL not found in environment variables")
engine = create_engine(database_url)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/login")
def login():
    auth_url = auth_manager.get_authorize_url()
    return redirect(auth_url)


@app.route("/callback")
def callback():
    try:
        code = request.args.get("code")
        if not code:
            return "No code in request", 400

        # get access token for this user
        token_info = auth_manager.get_access_token(code, as_dict=True)
        access_token = token_info["access_token"]

        # get Spotify user id
        import spotipy
        sp = spotipy.Spotify(auth=access_token)
        user_id = sp.current_user()["id"]
        session['user_id'] = user_id  # store in session

        # run ETL for this user
        extract_tracks(access_token)          # creates raw_spotify.json
        df = clean_data()                     # returns clean_spotify.csv as DataFrame
        load_sql(df, user_id)                 # load into user-specific table

        return redirect(url_for("home"))

    except Exception as e:
        import traceback
        traceback.print_exc()
        return f"Internal Server Error: {str(e)}", 500


@app.route("/tracks/sql")
def get_sql_tracks():
    user_id = session.get('user_id')
    if not user_id:
        return {"error": "User not logged in"}, 401

    table_name = f"tracks_{user_id}"
    try:
        df = pd.read_sql(f"SELECT * FROM {table_name}", engine)
        return df.to_json(orient="records")
    except Exception as e:
        return {"error": str(e)}, 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
