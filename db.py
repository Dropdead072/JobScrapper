import sqlite3
import hashlib
from datetime import datetime

DB_PATH = "db\\jobs.db"  # база лежит прямо в папке проекта


def url_to_hash(url: str) -> str:
    """Считаем хэш от url (обрезаем для компактности)"""
    full_hash = hashlib.sha256(url.encode("utf-8")).hexdigest()
    return full_hash[:24]


def db_init():
    """Создаём таблицу если её нет"""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS vacancies (
        url_hash TEXT PRIMARY KEY,
        url TEXT UNIQUE,
        title TEXT,
        company TEXT,
        description TEXT,
        date_added TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    cur.close()
    conn.close()


def add_to_db(url: str, title: str, company: str, description: str = None):
    """Добавляем запись (url как primary key через hash)"""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    url_hash = url_to_hash(url)

    try:
        cur.execute("""
            INSERT INTO vacancies (url_hash, url, title, description, company, date_added)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (url_hash, url, title, description, company, datetime.now()))
    except sqlite3.IntegrityError:
        print(f"[skip] Уже есть запись для {url}")

    conn.commit()
    cur.close()
    conn.close()


def drop_from_db(url: str):
    """Удаляем запись по url"""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("DELETE FROM vacancies WHERE url = ?", (url,))

    conn.commit()
    cur.close()
    conn.close()


def update_description(url: str, description: str):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
        UPDATE vacancies
        SET description = ?
        WHERE url = ?
    """, (description, url))

    conn.commit()
    cur.close()
    conn.close()


if __name__ == "__main__":
    db_init()
    add_to_db("https://example.com/job1", "Data Scientist", "Cool job at Example")
    drop_from_db("https://example.com/job1")
