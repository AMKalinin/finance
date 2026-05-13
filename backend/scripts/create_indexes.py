#!/usr/bin/env python3
"""
Скрипт для принудительного создания индексов в базе данных Finance Backend.
Используется когда таблицы уже существуют и нужно добавить новые индексы.

Запуск: poetry run python scripts/create_indexes.py
"""

from app.db.session import engine, SessionLocal
from app.db.base_class import Base
from sqlalchemy import text


def create_indexes():
    """Создает все необходимые индексы в базе данных."""
    
    print("🚀 Создание индексов базы данных...")
    
    # Инструкции для создания индексов (SQLite совместимые)
    index_sql = [
        # Account
        "CREATE INDEX IF NOT EXISTS ix_account_user_is_deleted ON account(user_id, is_deleted);",
        "CREATE INDEX IF NOT EXISTS ix_account_user_archived ON account(user_id, is_archived);",
        "CREATE INDEX IF NOT EXISTS ix_account_user_primary ON account(user_id, is_primary);",
        "CREATE INDEX IF NOT EXISTS ix_account_type ON account(account_type);",
        
        # Category
        "CREATE INDEX IF NOT EXISTS ix_category_user_type ON category(user_id, type);",
        "CREATE INDEX IF NOT EXISTS ix_category_parent_level ON category(parent_id, level);",
        "CREATE INDEX IF NOT EXISTS ix_category_user_is_deleted ON category(user_id, is_deleted);",
        
        # Transaction
        "CREATE INDEX IF NOT EXISTS ix_transaction_date ON transaction(date);",
        "CREATE INDEX IF NOT EXISTS ix_transaction_account_type ON transaction(from_account_id, to_account_id, type);",
        "CREATE INDEX IF NOT EXISTS ix_transaction_category_status ON transaction(category, status);",
        
        # Transaction_distribution_user
        "CREATE INDEX IF NOT EXISTS ix_transaction_dist_user_status ON transaction_distribution_user(user_id, is_deleted);",
        "CREATE INDEX IF NOT EXISTS ix_transaction_dist_role_status ON transaction_distribution_user(distribution_user_role, distribution_status);",
        
        # Friends
        "CREATE INDEX IF NOT EXISTS ix_friends_user1_status ON friends(user1_id, status);",
        "CREATE INDEX IF NOT EXISTS ix_friends_user2_status ON friends(user2_id, status);",
        
        # Position
        "CREATE INDEX IF NOT EXISTS ix_position_transaction ON position(transaction_id);",
        
        # Position_user
        "CREATE INDEX IF NOT EXISTS ix_position_user_position ON position_user(position_id);",
        "CREATE INDEX IF NOT EXISTS ix_position_user_user ON position_user(user_id);",
        
        # User
        "CREATE INDEX IF NOT EXISTS ix_user_subscription_type ON user(subscription_type);",
    ]
    
    db = SessionLocal()
    try:
        created_count = 0
        
        for sql in index_sql:
            result = db.execute(text(sql))
            if result.rowcount > 0 or "created" in str(result).lower():
                print(f"✅ Создан индекс")
                created_count += 1
            else:
                # SQLite не возвращает rowcount для CREATE INDEX, проверяем иначе
                print(f"ℹ️ Индекс уже существует или создан")
        
        db.commit()
        print(f"\n✅ Готово! Всего создано/найдено индексов: {created_count}")
        
    except Exception as e:
        db.rollback()
        print(f"\n❌ Ошибка при создании индексов: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    create_indexes()
