import sqlite3
import os
from pathlib import Path

APP_NAME = "FileTar"

def get_db_path():
    # biztos AppData elérés
    appdata = os.environ.get("APPDATA")

    if not appdata:
        # fallback PyInstaller / edge case
        appdata = str(Path.home() / "AppData" / "Roaming")

    base = os.path.join(appdata, "MonkerSoft", APP_NAME)
    os.makedirs(base, exist_ok=True)

    return os.path.join(base, "filetar.db")


DB = get_db_path()


def connect():
    return sqlite3.connect(DB)


def init_db():
    conn = connect()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS files (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        code TEXT UNIQUE,
        name TEXT,
        server TEXT,
        path TEXT
    )
    """)

    conn.commit()
    conn.close()