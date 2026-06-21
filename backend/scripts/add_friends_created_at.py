#!/usr/bin/env python3
"""Миграция: добавление колонки created_at в таблицу friends (для SQLite)."""

import sqlite3
import sys
import os

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "finance_db.sqlite")
DB_PATH = os.path.normpath(DB_PATH)


def migrate():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Проверяем, есть ли уже колонка
    cursor.execute("PRAGMA table_info(friends)")
    columns = {row[1] for row in cursor.fetchall()}

    if "created_at" not in columns:
        print("Добавление колонки created_at в таблицу friends (SQLite)...")

        # Копируем данные в новую таблицу
        cursor.execute("SELECT user1_id, user2_id, status FROM friends")
        rows = cursor.fetchall()

        cursor.execute("""
            CREATE TABLE friends_new (
                user1_id TEXT NOT NULL,
                user2_id TEXT NOT NULL,
                status TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                PRIMARY KEY (user1_id, user2_id),
                FOREIGN KEY (user1_id) REFERENCES user (id),
                FOREIGN KEY (user2_id) REFERENCES user (id)
            )
        """)

        if rows:
            cursor.executemany(
                "INSERT INTO friends_new (user1_id, user2_id, status) VALUES (?, ?, ?)",
                rows,
            )

        cursor.execute("DROP TABLE IF EXISTS friends")
        cursor.execute("ALTER TABLE friends_new RENAME TO friends")

        # Восстанавливаем индексы
        cursor.execute(
            "CREATE INDEX IF NOT EXISTS ix_friends_user1_status ON friends (user1_id, status)"
        )
        cursor.execute(
            "CREATE INDEX IF NOT EXISTS ix_friends_user2_status ON friends (user2_id, status)"
        )

        conn.commit()
        print("✅ Колонка created_at добавлена.")
    else:
        print("Колонка created_at уже существует.")

    conn.close()


if __name__ == "__main__":
    db_path = sys.argv[1] if len(sys.argv) > 1 else None
    if db_path:
        DB_PATH = os.path.normpath(db_path)
    migrate()
