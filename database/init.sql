CREATE TABLE IF NOT EXISTS tracks (
    id TEXT PRIMARY KEY,
    name TEXT,
    artist TEXT,
    album TEXT,
    popularity INT,
    duration_ms INT,
    release_date TEXT,
    duration_min FLOAT,
    release_year TEXT
);