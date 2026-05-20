import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import csv
from database import connect


class FileTarGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("FileTár")
        self.root.geometry("900x550")

        # ===== TOP BAR =====
        top = tk.Frame(root)
        top.pack(fill=tk.X)

        tk.Label(top, text="Keresés:").pack(side=tk.LEFT)

        self.search = tk.Entry(top)
        self.search.pack(side=tk.LEFT)

        tk.Button(top, text="Keres", command=self.search_data).pack(side=tk.LEFT)
        tk.Button(top, text="Frissít", command=self.load).pack(side=tk.LEFT)
        tk.Button(top, text="Export CSV", command=self.export).pack(side=tk.LEFT)
        tk.Button(top, text="Új rekord", command=self.open_add).pack(side=tk.LEFT)

        # ===== TABLE =====
        self.tree = ttk.Treeview(root, columns=("code","name","server","path"), show="headings")

        for c in ("code","name","server","path"):
            self.tree.heading(c, text=c)
            self.tree.column(c, width=200)

        self.tree.pack(fill=tk.BOTH, expand=True)

        self.load()

    # ===== LOAD =====
    def load(self):
        self.tree.delete(*self.tree.get_children())

        conn = connect()
        cur = conn.cursor()
        cur.execute("SELECT code, name, server, path FROM files")

        for row in cur.fetchall():
            self.tree.insert("", "end", values=row)

        conn.close()

    # ===== SEARCH =====
    def search_data(self):
        q = self.search.get()

        self.tree.delete(*self.tree.get_children())

        conn = connect()
        cur = conn.cursor()

        cur.execute("""
        SELECT code, name, server, path FROM files
        WHERE code LIKE ? OR name LIKE ? OR server LIKE ?
        """, (f"%{q}%", f"%{q}%", f"%{q}%"))

        for row in cur.fetchall():
            self.tree.insert("", "end", values=row)

        conn.close()

    # ===== ADD WINDOW =====
    def open_add(self):
        win = tk.Toplevel(self.root)
        win.title("Új rekord")
        win.geometry("300x300")

        tk.Label(win, text="Kód").pack()
        code = tk.Entry(win)
        code.pack()

        tk.Label(win, text="Név").pack()
        name = tk.Entry(win)
        name.pack()

        tk.Label(win, text="Szerver").pack()
        server = tk.Entry(win)
        server.pack()

        tk.Label(win, text="Útvonal").pack()
        path = tk.Entry(win)
        path.pack()

        def save():
            conn = connect()
            cur = conn.cursor()

            cur.execute("""
            INSERT INTO files (code, name, server, path)
            VALUES (?, ?, ?, ?)
            """, (
                code.get(),
                name.get(),
                server.get(),
                path.get()
            ))

            conn.commit()
            conn.close()

            win.destroy()
            self.load()

        tk.Button(win, text="Mentés", command=save).pack(pady=10)

    # ===== EXPORT =====
    def export(self):
        file = filedialog.asksaveasfilename(defaultextension=".csv")
        if not file:
            return

        conn = connect()
        cur = conn.cursor()
        cur.execute("SELECT code, name, server, path FROM files")

        with open(file, "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(["code","name","server","path"])
            w.writerows(cur.fetchall())

        conn.close()
        messagebox.showinfo("FileTár", "Export kész")


def start_gui():
    root = tk.Tk()
    app = FileTarGUI(root)
    root.mainloop()