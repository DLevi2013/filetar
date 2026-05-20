import bcrypt
from database import connect


def hash_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())


def create_user(username, password, role="user"):
    conn = connect()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
        (username, hash_password(password), role)
    )

    conn.commit()
    conn.close()


def login(username, password):
    conn = connect()
    cur = conn.cursor()

    cur.execute("SELECT password, role FROM users WHERE username=?", (username,))
    result = cur.fetchone()

    conn.close()

    if not result:
        return None

    hashed, role = result

    if bcrypt.checkpw(password.encode(), hashed):
        return role

    return None