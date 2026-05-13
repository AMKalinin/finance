#!/usr/bin/env python3
"""
Скрипт для проверки созданных индексов в базе данных Finance Backend.
Используется для верификации после добавления новых таблиц или изменений схемы.

Запуск: poetry run python scripts/check_indexes.py
"""

from sqlalchemy import inspect
from app.db.session import engine
from app.db.base_class import Base


def check_indexes():
    """Проверяет все таблицы на наличие индексов."""
    
    # Таблицы для проверки
    tables = [
        'account',
        'category', 
        'transaction',
        'friends',
        'position',
        'position_user',
        'subscription_type',
        'user'
    ]
    
    inspector = inspect(engine)
    
    print("=" * 70)
    print("ПРОВЕРКА ИНДЕКСОВ БАЗЫ ДАННЫХ")
    print("=" * 70)
    
    all_indexes = []
    
    for table in tables:
        try:
            indexes = inspector.get_indexes(table)
            
            if not indexes:
                print(f"\n⚠️ {table.upper()}: Нет индексов!")
                continue
            
            # Первичные ключи
            pk_constraints = [c for c in inspector.get_pk_constraint(table)]
            
            print(f"\n{'='*70}")
            print(f"📊 ТАБЛИЦА: {table.upper()}")
            print(f"{'='*70}")
            
            # Индексы
            if indexes:
                print("\n📌 ИНДЕКСЫ:")
                for idx in indexes:
                    status = "✅" if idx["unique"] == False else "🔒 UNIQUE"
                    print(f"   {status} {idx['name']:40s} on columns: {', '.join(idx['column_names'])}")
            
            # Первичные ключи
            if pk_constraints:
                print("\n🔑 ПЕРВИЧНЫЕ КЛЮЧИ:")
                for pk in pk_constraints:
                    cols = ', '.join(pk.get('constrained_columns', []))
                    print(f"   🔐 {cols}")
            
            # Внешние ключи
            foreign_keys = inspector.get_foreign_keys(table)
            if foreign_keys:
                print("\n🔗 ВНЕШНИЕ КЛЮЧИ:")
                for fk in foreign_keys:
                    cols = ', '.join(fk.get('constrained_columns', []))
                    ref_table = fk.get('referred_table', 'unknown')
                    ref_cols = ', '.join(fk.get('referred_columns', []))
                    print(f"   ➡️ {cols} → {ref_table}.{ref_cols}")
            
            # Подсчет
            all_indexes.extend(indexes)
            
        except Exception as e:
            print(f"\n❌ Ошибка при чтении таблицы {table}: {e}")
    
    print("\n" + "=" * 70)
    print(f"ВСЕГО ИНДЕКСОВ НАЙДЕНО: {len(all_indexes)}")
    print("=" * 70)


def check_slow_queries():
    """Проверяет эффективность запросов с использованием индексов."""
    
    from sqlalchemy.orm import Session
    
    session = Session(engine)
    
    print("\n" + "=" * 70)
    print("ПРОВЕРКА ЭФФЕКТИВНОСТИ ЗАПРОСОВ")
    print("=" * 70)
    
    # Примеры запросов для проверки
    test_queries = [
        {
            "name": "Поиск активных счетов пользователя",
            "sql": """
                SELECT COUNT(*) FROM account 
                WHERE user_id IS NOT NULL AND is_deleted = false
            """,
        },
        {
            "name": "Поиск транзакций по дате",
            "sql": """
                SELECT COUNT(*) FROM transaction 
                WHERE date >= '2025-01-01'
            """,
        },
    ]
    
    for query in test_queries:
        try:
            result = session.execute(query["sql"])
            count = result.scalar()
            
            # Получаем план выполнения (только для SQLite)
            explain_sql = f"EXPLAIN QUERY PLAN {query['sql']}"
            plan_result = session.execute(explain_sql)
            plan_rows = plan_result.fetchall()
            
            print(f"\n📋 {query['name']}")
            print(f"   Результат: {count} записей")
            print(f"   План выполнения:")
            for row in plan_rows[:3]:  # Показываем первые 3 строки плана
                print(f"      - {row}")
                
        except Exception as e:
            print(f"\n❌ Ошибка при проверке: {e}")


if __name__ == "__main__":
    check_indexes()
    check_slow_queries()
