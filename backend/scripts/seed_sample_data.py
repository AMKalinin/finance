"""
Скрипт для заполнения базы данных тестовыми данными (счета и категории).
Запускается после создания БД.
"""

import sys
from datetime import date, timedelta
from uuid import uuid4

# Добавляем путь к приложению
sys.path.insert(0, '/home/alex/Documents/finance/backend/app')

from core.config import settings
from db.base_class import Base
from models.account import Account
from models.category import Category
from schemas.account import account_in
from schemas.category import category_in


def create_sample_accounts():
    """Создаем тестовые счета для пользователя."""
    print("📊 Создание тестовых счетов...")
    
    accounts = [
        {
            "name": "Сбербанк",
            "currency": "RUB",
            "balance": 50000.0,
            "account_type": "debit"
        },
        {
            "name": "Тинькофф",
            "currency": "RUB",
            "balance": 12345.67,
            "account_type": "savings"
        },
        {
            "name": "American Express",
            "currency": "USD",
            "balance": 2500.0,
            "account_type": "credit"
        },
        {
            "name": "Кредитная карта",
            "currency": "RUB",
            "balance": -15000.0,
            "account_type": "loan_owed"
        }
    ]
    
    for acc in accounts:
        account_data = account_in(
            name=acc["name"],
            currency=acc["currency"],
            balance=acc["balance"],
            account_type=acc["account_type"],
            description=f"{acc['name']} (тестовый счет)"
        )
        
        from crud.crud_account import CRUD_account
        crud = CRUD_account()
        db_acc = crud.create_account(account_data)
        print(f"  ✅ Создан счет: {db_acc.name} ({db_acc.currency})")


def create_sample_categories():
    """Создаем тестовые категории расходов и доходов."""
    print("📁 Создание тестовых категорий...")
    
    # Корневые категории расходов (expense)
    expense_categories = [
        {"name": "Еда", "type": "expense"},
        {"name": "Транспорт", "type": "expense"},
        {"name": "Жилье", "type": "expense"},
        {"name": "Здоровье", "type": "expense"},
        {"name": "Образование", "type": "expense"},
    ]
    
    # Корневые категории доходов (income)
    income_categories = [
        {"name": "Зарплата", "type": "income"},
        {"name": "Инвестиции", "type": "income"},
        {"name": "Подарки", "type": "income"},
    ]
    
    # Создаем категории расходов с подкатегориями
    for root_cat in expense_categories:
        cat_data = category_in(
            name=root_cat["name"],
            type=root_cat["type"],
            level=1,
            parent_category=None
        )
        
        from crud.crud_category import CRUD_category
        crud = CRUD_category()
        db_cat = crud.create_category(cat_data)
        
        # Создаем подкатегории для "Еда" и "Транспорт"
        if root_cat["name"] in ["Еда", "Транспорт"]:
            subs = [
                {"name": f"{root_cat['name']} - Еда на дом", "type": "expense"},
                {"name": f"{root_cat['name']} - Еда на вынос", "type": "expense"},
                {"name": f"{root_cat['name']} - Продукты", "type": "expense"} if root_cat["name"] == "Еда" else None,
                 {"name": f"{root_cat['name']} - Заправка", "type": "expense"} if root_cat["name"] == "Транспорт" else None,
            ]
            
            for sub in subs:
                if not sub:
                    continue
                sub_data = category_in(
                    name=sub["name"],
                    type=sub["type"],
                    level=2,
                    parent_category=db_cat.id
                )
                
                crud_sub = CRUD_category()
                db_sub = crud_sub.create_category(sub_data)
                print(f"  ✅ Создана подкатегория: {db_sub.name}")


    # Создаем категории доходов
    for root_cat in income_categories:
        cat_data = category_in(
            name=root_cat["name"],
            type=root_cat["type"],
            level=1,
            parent_category=None
        )
        
        crud = CRUD_category()
        db_cat = crud.create_category(cat_data)
        print(f"  ✅ Создана категория: {db_cat.name}")


def main():
    """Основная функция для заполнения БД."""
    from app.db.init_db import init_db
    
    # Инициализируем базу данных
    init_db()
    
    # Создаем тестовые счета
    create_sample_accounts()
    
    # Создаем тестовые категории
    create_sample_categories()
    
    print("\n✅ Заполнение базы данных завершено!")


if __name__ == "__main__":
    main()
