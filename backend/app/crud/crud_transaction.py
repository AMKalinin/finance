from datetime import date
from uuid import UUID
from typing import List

from app.crud.crud_base import CRUD_base
from app.models.transaction import Transaction
from app.schemas.transaction import (
    transaction_in,
    transaction_in_date,
    transaction_in_description,
    transaction_in_size,
)


class CRUD_transaction(CRUD_base):

    def create_transaction(self, transaction_info: transaction_in) -> Transaction:
        db_transaction = Transaction(
            from_account_id=transaction_info.FROM,
            to_account_id=transaction_info.TO,
            category=transaction_info.category,
            type=transaction_info.type,
            debit_size=transaction_info.debit_size,
            credit_size=transaction_info.credit_size,
            exchange_rate=transaction_info.exchange_rate,
            date=transaction_info.date,
            split_type=transaction_info.split_type,
            status=transaction_info.status if transaction_info.status else 'pending',
            description=transaction_info.description,
        )
        self.db.add(db_transaction)
        self.db.flush()
        return db_transaction

    def get_by_id(self, id: UUID) -> Transaction | None:
        """Получить транзакцию по ID (если пользователь участвует в ней)."""
        distr = (
            self.db.query(Transaction)
            .join(
                Transaction.transaction_distribution_user,
            )
            .filter(
                Transaction.id == id,
                Transaction.transaction_distribution_user.any(user_id=self.user.id),
            )
            .first()
        )
        return distr

    def get_all_transaction(self, skip: int = 0, limit: int = 100) -> List[Transaction]:
        """
        Получить все транзакции пользователя с пагинацией.
        
        Args:
            skip: Количество записей для пропуска
            limit: Максимальное количество записей
        
        Returns:
            Список транзакций пользователя
        """
        return (
            self.db.query(Transaction)
            .join(Transaction.transaction_distribution_user)
            .filter(
                Transaction.transaction_distribution_user.any(
                    user_id=self.user.id, is_deleted=False
                )
            )
            .distinct(Transaction.id)
            .offset(skip)
            .limit(limit)
            .all()
        )
    
    def count_all(self) -> int:
        """Получить общее количество транзакций пользователя."""
        return (
            self.db.query(Transaction)
            .join(Transaction.transaction_distribution_user)
            .filter(
                Transaction.transaction_distribution_user.any(
                    user_id=self.user.id, is_deleted=False
                )
            )
            .distinct(Transaction.id)
            .count()
        )

    def get_all_transaction_for_period(
        self,
        from_date: date,
        to_date: date,
        skip: int = 0,
        limit: int = 100
    ) -> List[Transaction]:
        """
        Получить транзакции пользователя за период с пагинацией.
        
        Args:
            from_date: Дата начала периода
            to_date: Дата окончания периода
            skip: Количество записей для пропуска
            limit: Максимальное количество записей
        
        Returns:
            Список транзакций за указанный период
        """
        return (
            self.db.query(Transaction)
            .join(Transaction.transaction_distribution_user)
            .filter(
                Transaction.transaction_distribution_user.any(
                    user_id=self.user.id, is_deleted=False
                ),
                Transaction.date >= from_date,
                Transaction.date <= to_date,
            )
            .distinct(Transaction.id)
            .offset(skip)
            .limit(limit)
            .all()
        )
    
    def count_all_for_period(self, from_date: date, to_date: date) -> int:
        """Получить общее количество транзакций за период."""
        return (
            self.db.query(Transaction)
            .join(Transaction.transaction_distribution_user)
            .filter(
                Transaction.transaction_distribution_user.any(
                    user_id=self.user.id, is_deleted=False
                ),
                Transaction.date >= from_date,
                Transaction.date <= to_date,
            )
            .distinct(Transaction.id)
            .count()
        )

    def get_all_transaction_for_period_with_type(
        self,
        from_date: date,
        to_date: date,
        type_name: str,
        skip: int = 0,
        limit: int = 100
    ) -> List[Transaction]:
        """
        Получить транзакции пользователя за период с фильтрацией по типу и пагинацией.
        
        Args:
            from_date: Дата начала периода
            to_date: Дата окончания периода
            type_name: Тип операции (debit, adding, transfer)
            skip: Количество записей для пропуска
            limit: Максимальное количество записей
        
        Returns:
            Список транзакций с фильтрацией по типу
        """
        return (
            self.db.query(Transaction)
            .join(Transaction.transaction_distribution_user)
            .filter(
                Transaction.transaction_distribution_user.any(
                    user_id=self.user.id, is_deleted=False
                ),
                Transaction.date >= from_date,
                Transaction.date <= to_date,
                Transaction.type == type_name,
            )
            .distinct(Transaction.id)
            .offset(skip)
            .limit(limit)
            .all()
        )
    
    def count_all_for_period_with_type(
        self, from_date: date, to_date: date, type_name: str
    ) -> int:
        """Получить общее количество транзакций за период с фильтром по типу."""
        return (
            self.db.query(Transaction)
            .join(Transaction.transaction_distribution_user)
            .filter(
                Transaction.transaction_distribution_user.any(
                    user_id=self.user.id, is_deleted=False
                ),
                Transaction.date >= from_date,
                Transaction.date <= to_date,
                Transaction.type == type_name,
            )
            .distinct(Transaction.id)
            .count()
        )

    def update_size(self, transaction_info: transaction_in_size) -> Transaction:
        """Обновить размер транзакции (debit_size)."""
        db_transaction = self.db.query(Transaction).get(transaction_info.id)
        if db_transaction is None:
            return None

        db_transaction.debit_size = transaction_info.size
        return db_transaction

    def update_date(self, transaction_info: transaction_in_date) -> Transaction:
        db_transaction = self.db.query(Transaction).get(transaction_info.id)
        if db_transaction is None:
            return None

        db_transaction.date = transaction_info.date
        return db_transaction

    def update_description(self, transaction_info: transaction_in_description) -> Transaction:
        db_transaction = self.db.query(Transaction).get(transaction_info.id)
        if db_transaction is None:
            return None

        db_transaction.description = transaction_info.description
        return db_transaction

    def delete(self, id: UUID) -> Transaction:
        """Получить транзакцию перед удалением (для возврата из endpoint)."""
        db_transaction = self.db.query(Transaction).get(id)
        if db_transaction is None:
            return None
        self.db.delete(db_transaction)
        return db_transaction
