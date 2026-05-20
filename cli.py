from database import connect
import os


def add_file():
    print("\n--- ÚJ REKORD ---")

    code = input("Kód (pl. K3297): ")
    name = input("Név: ")
    server = input("Szerver: ")
    path = input("UNC útvonal: ")

    conn = connect()
    cur = conn.cursor()

    cur.execute("""
    INSERT INTO files (code, name, server, path)
    VALUES (?, ?, ?, ?)
    """, (code, name, server, path))

    conn.commit()
    conn.close()

    print("OK: mentve\n")


def list_files():
    conn = connect()
    cur = conn.cursor()

    cur.execute("SELECT code, name, server, path FROM files")
    rows = cur.fetchall()

    conn.close()

    print("\n--- LISTA ---")
    for r in rows:
        print(f"{r[0]} | {r[1]} | {r[2]} | {r[3]}")


def search():
    q = input("Keresés: ")

    conn = connect()
    cur = conn.cursor()

    cur.execute("""
    SELECT code, name, server, path FROM files
    WHERE code LIKE ? OR name LIKE ? OR server LIKE ?
    """, (f"%{q}%", f"%{q}%", f"%{q}%"))

    rows = cur.fetchall()
    conn.close()

    print("\n--- TALÁLATOK ---")
    for r in rows:
        print(f"{r[0]} | {r[1]} | {r[2]} | {r[3]}")


def open_file():
    code = input("Kód: ")

    conn = connect()
    cur = conn.cursor()

    cur.execute("SELECT path FROM files WHERE code=?", (code,))
    row = cur.fetchone()

    conn.close()

    if row:
        try:
            os.startfile(row[0])
        except:
            print("Nem sikerült megnyitni a fájlt.")
    else:
        print("Nincs ilyen rekord.")


def run_cli():
    while True:
        print("\n====================")
        print(" FileTár CLI")
        print("====================")
        print("1 - Új rekord")
        print("2 - Lista")
        print("3 - Keresés")
        print("4 - Megnyitás")
        print("0 - Kilépés")

        c = input("> ")

        if c == "1":
            add_file()

        elif c == "2":
            list_files()

        elif c == "3":
            search()

        elif c == "4":
            open_file()

        elif c == "0":
            break