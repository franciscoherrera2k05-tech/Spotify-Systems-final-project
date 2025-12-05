from flask import Flask, redirect, request, url_for, render_template
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
app.secret_key = "replace_with_your_secret"
CORS(app)

auth_manager = SpotifyOAuth(
   client_id=os.getenv("SPOTIPY_CLIENT_ID"),
   client_secret=os.getenv("SPOTIPY_CLIENT_SECRET"),
   redirect_uri=os.getenv("REDIRECT_URL"),
   scope="user-top-read",
   cache_path=".cache"
)

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

       token_info = auth_manager.get_access_token(code, as_dict=True)
       access_token = token_info["access_token"]

       #run ETL using the required token
       extract_tracks(access_token)
       clean_data()
       load_sql()

       return redirect(url_for("home"))

   except Exception as e:
       import traceback
       traceback.print_exc()
       return f"Internal Server Error: {str(e)}", 500

@app.route("/tracks/sql")
def get_sql_tracks():
   db_user = os.getenv("POSTGRES_USER")
   db_password = os.getenv("POSTGRES_PASSWORD")
   db_name = os.getenv("POSTGRES_DB")
   engine = create_engine(f"postgresql://{db_user}:{db_password}@postgres:5432/{db_name}")
   df = pd.read_sql("SELECT * FROM tracks", engine)
   return df.to_json(orient="records")

if __name__ == "__main__":
   app.run(host="0.0.0.0", port=5000)
