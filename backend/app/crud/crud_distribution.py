from uuid import UUID
from typing import List

from app.crud.crud_base import CRUD_base
from app.models.transaction_distribution_user import Transaction_distribution_user
from app.schemas.distribution import distribution_in, distribution_settle_in
from app.err.errors import DistributionNotFoundError, TransactionNotFoundError


class CRUD_distribution(CRUD_base):

    def create_distribution(self, distribution: distribution_in) -> Transaction_distribution_user:
        """Создать распределение для пользователя."""
        # Проверяем, нет ли уже такого распределения
        existing = self.db.query(Transaction_distribution_user).filter_by(
            transaction_id=distribution.transaction_id,
            user_id=distribution.user_id,
            is_deleted=False
        ).first()

        if existing:
            # Обновляем существующее вместо создания дубликата
            if distribution.size is not None:
                existing.size = distribution.size
            return existing

        db_distr = Transaction_distribution_user(
            user_id=distribution.user_id,
            transaction_id=distribution.transaction_id,
            distribution_user_role=distribution.role,
            size=distribution.size,
            distribution_status='pending'
        )
        self.db.add(db_distr)
        return db_distr

    def get_distributions_for_transaction(self, transaction_id: UUID) -> List[Transaction_distribution_user]:
        """Получить все активные распределения транзакции."""
        return (
            self.db.query(Transaction_distribution_user)
            .filter_by(transaction_id=transaction_id, is_deleted=False)
            .all()
        )

    def get_distribution(
        self, transaction_id: UUID, user_id: UUID
    ) -> Transaction_distribution_user:
        """Получить конкретное распределение пользователя по транзакции."""
        db_distr = (
            self.db.query(Transaction_distribution_user)
            .filter_by(
                transaction_id=transaction_id,
                user_id=user_id,
                is_deleted=False
            )
            .first()
        )
        if db_distr is None:
            raise DistributionNotFoundError(
                f"Распределение для user={user_id}, transaction={transaction_id} не найдено"
            )
        return db_distr

    def get_distribution_by_pk(
        self, transaction_id: UUID, user_id: UUID
    ) -> Transaction_distribution_user | None:
        """Получить распределение по первичному ключу (может быть soft-deleted)."""
        return (
            self.db.query(Transaction_distribution_user)
            .filter_by(transaction_id=transaction_id, user_id=user_id)
            .first()
        )

    def update_distribution(self, distribution_info: distribution_in) -> Transaction_distribution_user:
        """Обновить размер распределения."""
        db_distr = (
            self.db.query(Transaction_distribution_user)
            .filter_by(
                transaction_id=distribution_info.transaction_id,
                user_id=distribution_info.user_id,
                is_deleted=False
            )
            .first()
        )
        if db_distr is None:
            raise DistributionNotFoundError("Распределение не найдено")

        if distribution_info.size is not None:
            db_distr.size = distribution_info.size

        return db_distr

    def settle_distribution(self, settle_info: distribution_settle_in) -> Transaction_distribution_user:
        """Пометить распределение как оплаченное."""
        db_distr = (
            self.db.query(Transaction_distribution_user)
            .filter_by(
                transaction_id=settle_info.transaction_id,
                user_id=settle_info.user_id,
                is_deleted=False
            )
            .first()
        )
        if db_distr is None:
            raise DistributionNotFoundError("Распределение не найдено")

        db_distr.distribution_status = 'settled'
        return db_distr

    def delete_distribution(self, distribution_info: distribution_in) -> Transaction_distribution_user:
        """Soft-delete распределения."""
        db_distr = (
            self.db.query(Transaction_distribution_user)
            .filter_by(
                transaction_id=distribution_info.transaction_id,
                user_id=distribution_info.user_id,
                is_deleted=False
            )
            .first()
        )
        if db_distr is None:
            raise DistributionNotFoundError("Распределение не найдено")

        db_distr.is_deleted = True
        return db_distr

    def delete_all_distributions(self, transaction_id: UUID) -> int:
        """Soft-delete всех распределений транзакции. Возвращает кол-во удалённых."""
        distributions = (
            self.db.query(Transaction_distribution_user)
            .filter_by(transaction_id=transaction_id, is_deleted=False)
            .all()
        )
        count = 0
        for distr in distributions:
            distr.is_deleted = True
            count += 1
        return count

    def get_total_distributed(self, transaction_id: UUID) -> float:
        """Сумма всех активных распределений транзакции."""
        distributions = self.get_distributions_for_transaction(transaction_id)
        total = 0.0
        for distr in distributions:
            if distr.size is not None:
                total += distr.size
        return total

    def recalculate_transaction_status(self, transaction_id: UUID) -> str:
        """
        Пересчитать статус транзакции на основе статусов распределений.
        Returns: 'pending', 'partially_paid', 'settled'
        """
        from app.models.transaction import Transaction

        distributions = self.get_distributions_for_transaction(transaction_id)
        if not distributions:
            return 'pending'

        all_statuses = [d.distribution_status for d in distributions]
        if all(s == 'settled' for s in all_statuses):
            new_status = 'settled'
        elif any(s == 'settled' for s in all_statuses):
            new_status = 'partially_paid'
        else:
            new_status = 'pending'

        # Обновляем статус транзакции в БД
        db_transaction = self.db.query(Transaction).get(transaction_id)
        if db_transaction:
            db_transaction.status = new_status

        return new_status
