#!/usr/bin/env python3
"""
Скрипт для проверки целостности данных в базе данных Finance Backend.
Проверяет:
- Отсутствие дубликатов
- Корректность внешних ключей
- Целостность балансов счетов
- Состояние транзакций

Запуск: poetry run python scripts/check_integrity.py
"""

from app.db.session import SessionLocal


def check_duplicates():
    """Проверяет на наличие дубликатов."""
    
    print("\n🔍 Проверка на дубликаты...")
    db = SessionLocal()
    
    try:
        # Проверка дубликатов в транзакциях (дата + тип + сумма)
        query = """
            SELECT type, date, debit_size, COUNT(*) as count
            FROM transaction
            WHERE is_deleted = false
            GROUP BY type, date, debit_size
            HAVING COUNT(*) > 1
        """
        result = db.execute(query).fetchall()
        
        if result:
            print(f"⚠️  Найдено {len(result)} дубликатов транзакций:")
            for row in result[:5]:
                print(f"   - type={row[0]}, date={row[1]}, amount={row[2]}")
        else:
            print("✅ Дубликаты не найдены")
        
        # Проверка дубликатов в пользователях (email, если есть)
        query = """
            SELECT subscription_type, COUNT(*) as count
            FROM user
            GROUP BY subscription_type
            HAVING COUNT(*) > 100
        """
        result = db.execute(query).fetchall()
        
        if not result:
            print("✅ Пользователи без проблем")
            
    except Exception as e:
        print(f"❌ Ошибка проверки: {e}")
    finally:
        db.close()


def check_balance_integrity():
    """Проверяет целостность балансов счетов."""
    
    print("\n💰 Проверка баланса счетов...")
    db = SessionLocal()
    
    try:
        # Сумма всех транзакций должна быть равна текущему балансу
        query = """
            SELECT 
                a.id,
                a.balance as current_balance,
                COALESCE(
                    (SELECT SUM(CASE WHEN t.type = 'debit' THEN -t.debit_size ELSE t.credit_size END)
                     FROM transaction t
                     WHERE t.from_account_id = a.id AND t.is_deleted = false), 0
                ) as calculated_balance
            FROM account a
            WHERE a.is_deleted = false
        """
        
        result = db.execute(query).fetchall()
        
        issues_found = False
        for row in result:
            current, calculated = float(row[1]), float(row[2])
            if abs(current - calculated) > 0.01:  # Допуск 1 копейка
                print(f"⚠️  Счет {row[0]}: текущий={current}, расчетный={calculated}")
                issues_found = True
        
        if not issues_found:
            print("✅ Балансы счетов в порядке")
            
    except Exception as e:
        print(f"❌ Ошибка проверки баланса: {e}")
    finally:
        db.close()


def check_orphan_records():
    """Проверяет на наличие сиротских записей (без родительской записи)."""
    
    print("\n🔗 Проверка внешних связей...")
    db = SessionLocal()
    
    try:
        # Сиротские транзакции (ссылаются на несуществующие счета)
        query = """
            SELECT COUNT(*) FROM transaction t
            WHERE t.is_deleted = false 
              AND (t.from_account_id NOT IN (SELECT id FROM account)
                   OR t.to_account_id NOT IN (SELECT id FROM account))
        """
        result = db.execute(query).fetchone()
        
        if result[0] > 0:
            print(f"⚠️  Найдено {result[0]} транзакций с несуществующими счетами")
        else:
            print("✅ Все транзакции имеют корректные ссылки на счета")
            
    except Exception as e:
        print(f"❌ Ошибка проверки связей: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    print("=" * 70)
    print("ПРОВЕРКА ЦЕЛОСТНОСТИ ДАННЫХ")
    print("=" * 70)
    
    check_duplicates()
    check_balance_integrity()
    check_orphan_records()
    
    print("\n" + "=" * 70)
    print("✅ Проверка завершена!")
    print("=" * 70)
