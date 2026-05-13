#!/usr/bin/env python3
"""
Скрипт для полной очистки базы данных Finance Backend.
Удаляет ВСЕ данные, но сохраняет структуру таблиц и индексы.

⚠️ ВНИМАНИЕ: Это действие необратимо!

Запуск: poetry run python scripts/clean_db.py
"""

from app.db.session import SessionLocal


def clean_database():
    """Полная очистка базы данных (сохраняет структуру)."""
    
    print("⚠️  ВНИМАНИЕ! Будет удалено ВСЕ данные из базы!")
    confirmation = input("Подтвердите удаление (напишите 'YES'): ")
    
    if confirmation != "YES":
        print("❌ Операция отменена")
        return
    
    db = SessionLocal()
    
    try:
        # Таблицы в порядке удаления (с учётом внешних ключей)
        tables_to_clean = [
            'transaction_distribution_user',  # Зависит от transaction и user
            'position_user',                   # Зависит от position и user
            'friends',                         # Зависит от user
            'position',                        # Зависит от transaction
            'transaction',                     # Самая главная таблица
            'account',                         # Зависит от user
            'category',                        # Зависит от user и self
            'user',                            # Зависимости от других таблиц
        ]
        
        print("\n🗑️  Очистка таблиц...")
        
        for table in tables_to_clean:
            try:
                db.execute(f"DELETE FROM {table}")
                print(f"   ✅ {table} очищена")
            except Exception as e:
                print(f"   ⚠️  {table}: {e}")
        
        db.commit()
        print("\n✅ База данных успешно очищена!")
        print("📊 Структура таблиц и индексы сохранены.")
        
    except Exception as e:
        db.rollback()
        print(f"\n❌ Ошибка при очистке базы: {e}")
        raise
    finally:
        db.close()


def drop_all_tables():
    """Полное удаление всех таблиц (создаст заново)."""
    
    print("⚠️  ВНИМАНИЕ! Будут удалены ВСЕ таблицы!")
    confirmation = input("Подтвердите удаление (напишите 'YES'): ")
    
    if confirmation != "YES":
        print("❌ Операция отменена")
        return
    
    from app.db.base_class import Base
    
    try:
        print("\n🗑️  Удаление всех таблиц...")
        Base.metadata.drop_all()
        
        print("\n✅ Все таблицы удалены!")
        print("💡 Для создания заново выполните:")
        print("   poetry run python -c \"from app.db.base_class import Base; from app.db.session import engine; Base.metadata.create_all(bind=engine)\"")
        
    except Exception as e:
        print(f"\n❌ Ошибка при удалении таблиц: {e}")


if __name__ == "__main__":
    mode = input("Выберите режим (1 - очистка данных, 2 - удаление таблиц): ")
    
    if mode == "1":
        clean_database()
    elif mode == "2":
        drop_all_tables()
    else:
        print("❌ Неверный выбор")
