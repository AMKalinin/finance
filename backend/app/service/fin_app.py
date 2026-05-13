from uuid import UUID
from datetime import date
from sqlalchemy.orm import Session

from app.crud import Crud
from app.core.utils import commit
from app.err.errors import (
    CreateCategoryError,
    SubscriptionError,
    MaxCategoryLevelError,
    DistributionError,
    TransactionNotFoundError,
    AccountLimitError,
    CategoryLimitError,
    TransactionDailyLimitError,
)
from app.models.account import Account
from app.models.category import Category
from app.models.transaction import Transaction
from app.schemas.account import (
    account_in,
    account_in_balance,
    account_in_description,
    account_in_name,
    account_in_primary,
    account_in_archived,
    account_in_decimal_places,
    account_in_emergency_fund,
    account_in_interest_rate,
)
from app.schemas.category import category_in, category_in_name
from app.schemas.position import position_in
from app.schemas.transaction import (
    distribution_in,
    transaction_in,
    transaction_in_date,
    transaction_in_description,
    transaction_in_size,
)
from app.schemas.distribution import distribution_settle_in


class Fin_app:
    def __init__(self, db: Session, user_info: dict) -> None:
        self.db: Session = db
        self.crud: Crud = Crud(self.db, user_info)
        self.user_info: dict = user_info

    # ------------------------------------------------------------------ #
    #                     Account operations                              #
    # ------------------------------------------------------------------ #

    def check_account_limit(self):
        """
        Проверить лимит на создание счетов для бесплатных пользователей.
        
        Free users: max 1 account
        Paid users: no limit
        """
        if self.user_info.get('subscription_type') == 'free':
            current_accounts = self.crud.account.count_all()
            if current_accounts >= 1:
                raise AccountLimitError(
                    "Бесплатные пользователи могут иметь только один счет. "
                    "Для создания дополнительных счетов оформите подписку."
                )
    
    @commit
    def create_account(self, account_info: account_in) -> Account:
        self.check_account_limit()
        account_info.balance = 0
        acc = self.crud.account.create_account(account_info)
        return acc

    def get_all_account(self, skip: int = 0, limit: int = 100) -> list[Account]:
        """
        Получить все учетные записи с пагинацией.
        
        Args:
            skip: Количество записей для пропуска
            limit: Максимальное количество записей
        
        Returns:
            Список учетных записей
        """
        return self.crud.account.get_all(skip=skip, limit=limit)
    
    def get_total_accounts(self) -> int:
        """Получить общее количество активных учетных записей."""
        return self.crud.account.count_all()

    def get_account_by_id(self, id: UUID) -> Account:
        return self.crud.account.get_by_id(id)

    @commit
    def update_account_balance(self, account_info: account_in_balance) -> Account:
        return self.crud.account.update_balance(account_info)

    @commit
    def update_account_name(self, account_info: account_in_name) -> Account:
        return self.crud.account.update_name(account_info)

    @commit
    def update_account_description(self, account_info: account_in_description) -> Account:
        return self.crud.account.update_description(account_info)

    @commit
    def update_account_interest_rate(self, account_info: account_in_interest_rate) -> Account:
        return self.crud.account.update_interest_rate(account_info)

    @commit
    def update_account_emergency_fund(
        self, account_info: account_in_emergency_fund
    ) -> Account:
        return self.crud.account.update_emergency_fund(account_info)

    @commit
    def update_account_decimal_places(
        self, account_info: account_in_decimal_places
    ) -> Account:
        return self.crud.account.update_decimal_places(account_info)

    @commit
    def update_account_archived(self, account_info: account_in_archived) -> Account:
        return self.crud.account.update_account_archived(account_info)

    @commit
    def update_account_primary(self, account_info: account_in_primary) -> Account:
        return self.crud.account.update_primary(account_info)

    def get_archived_accounts(self, skip: int = 0, limit: int = 100) -> list[Account]:
        """
        Получить архивированные учетные записи с пагинацией.
        
        Args:
            skip: Количество записей для пропуска
            limit: Максимальное количество записей
        
        Returns:
            Список архивированных учетных записей
        """
        return self.crud.account.get_archived(skip=skip, limit=limit)
    
    def get_total_archived_accounts(self) -> int:
        """Получить общее количество архивированных счетов."""
        return self.crud.account.count_archived()
    
    def get_primary_accounts(self, skip: int = 0, limit: int = 100) -> list[Account]:
        """
        Получить основные учетные записи с пагинацией.
        
        Args:
            skip: Количество записей для пропуска
            limit: Максимальное количество записей
        
        Returns:
            Список основных учетных записей
        """
        return self.crud.account.get_primary(skip=skip, limit=limit)
    
    def get_total_primary_accounts(self) -> int:
        """Получить общее количество основных счетов."""
        return self.crud.account.count_primary()
    
    @commit
    def delete_account(self, id: UUID) -> Account:
        return self.crud.account.delete(id)

    # ------------------------------------------------------------------ #
    #                     Category operations                             #
    # ------------------------------------------------------------------ #

    def get_category_by_id(self, id: UUID) -> Category:
        return self.crud.category.get_by_id(id)

    def get_all_category(self):
        return self.crud.category.get_all()

    def get_all_category_structured_list(self, skip: int = 0, limit: int = 100) -> list[Category]:
        """
        Получить все категории с пагинацией.
        
        Args:
            skip: Количество записей для пропуска
            limit: Максимальное количество записей
        
        Returns:
            Список категорий со структурой вложенности
        """
        return self.crud.category.get_all_structured_list(skip=skip, limit=limit)
    
    def get_total_categories(self) -> int:
        """Получить общее количество активных категорий."""
        return self.crud.category.count_all()
    
    def get_expense_categories(self, skip: int = 0, limit: int = 100) -> list[Category]:
        """
        Получить категории расходов с пагинацией.
        
        Args:
            skip: Количество записей для пропуска
            limit: Максимальное количество записей
        
        Returns:
            Список категорий расходов
        """
        return self.crud.category.get_by_type('expense', skip=skip, limit=limit)
    
    def get_total_expense_categories(self) -> int:
        """Получить общее количество категорий расходов."""
        return self.crud.category.count_by_type('expense')
    
    def get_income_categories(self, skip: int = 0, limit: int = 100) -> list[Category]:
        """
        Получить категории доходов с пагинацией.
        
        Args:
            skip: Количество записей для пропуска
            limit: Максимальное количество записей
        
        Returns:
            Список категорий доходов
        """
        return self.crud.category.get_by_type('income', skip=skip, limit=limit)
    
    def get_total_income_categories(self) -> int:
        """Получить общее количество категорий доходов."""
        return self.crud.category.count_by_type('income')

    def check_category_limit(self):
        """
        Проверить лимит на создание категорий для бесплатных пользователей.
        
        Free users: max 5 root categories (level=1), no nesting allowed
        Paid users: max 10 categories, can nest up to level 3
        """
        if self.user_info.get('subscription_type') == 'free':
            # Count only root-level categories for free users
            root_categories = (
                self.db.query(Category)
                .filter(
                    Category.user_id == self.user_info.get('id'),
                    Category.is_deleted == False,
                    Category.level == 1
                )
                .count()
            )
            if root_categories >= 5:
                raise CategoryLimitError(
                    "Бесплатные пользователи могут иметь только 5 категорий без вложенности. "
                    "Для создания дополнительных категорий или использования вложенности оформите подписку."
                )
    
    @commit
    def create_category(self, category_info: category_in):
        self.check_category_limit()
        all_category = self.get_all_category()
        if len(all_category) >= 10:
            raise SubscriptionError('Ограничения подписки')

        # For free users, check if they're trying to create nested categories
        if self.user_info.get('subscription_type') == 'free':
            if category_info.parent_category:
                parent_category = self.get_category_by_id(category_info.parent_category)
                if parent_category and not parent_category.is_deleted:
                    raise CategoryLimitError(
                        "Бесплатные пользователи не могут создавать вложенные категории. "
                        "Для использования вложенности оформите подписку."
                    )

        if category_info.parent_category:
            parent_category = self.get_category_by_id(category_info.parent_category)
            if parent_category:
                if parent_category.is_deleted:
                    raise CreateCategoryError('Родительская категория удалена')
                if parent_category.level == 3:
                    raise MaxCategoryLevelError('Превышен лимит вложенности категорий')
                category_info.level = parent_category.level + 1
                category_info.type = parent_category.type
        return self.crud.category.create_category(category_info)

    @commit
    def delete_category(self, id: UUID) -> Category:
        return self.crud.category.delete_category(id)

    @commit
    def update_category(self, category_info: category_in_name):
        return self.crud.category.update_name(category_info)

    # ------------------------------------------------------------------ #
    #                  Transaction operations                             #
    # ------------------------------------------------------------------ #

    def get_all_transaction(self, skip: int = 0, limit: int = 100) -> list[Transaction]:
        """
        Получить все транзакции с пагинацией.
        
        Args:
            skip: Количество записей для пропуска
            limit: Максимальное количество записей
        
        Returns:
            Список транзакций
        """
        return self.crud.transaction.get_all_transaction(skip=skip, limit=limit)
    
    def get_total_transactions(self) -> int:
        """Получить общее количество транзакций."""
        return self.crud.transaction.count_all()
    
    def get_all_transaction_for_period(
        self,
        from_date: date,
        to_date: date,
        skip: int = 0,
        limit: int = 100
    ) -> list[Transaction]:
        """
        Получить транзакции за период с пагинацией.
        
        Args:
            from_date: Дата начала
            to_date: Дата окончания
            skip: Количество записей для пропуска
            limit: Максимальное количество записей
        
        Returns:
            Список транзакций за указанный период
        """
        return self.crud.transaction.get_all_transaction_for_period(
            from_date, to_date, skip=skip, limit=limit
        )
    
    def get_total_transactions_for_period(self, from_date: date, to_date: date) -> int:
        """Получить общее количество транзакций за период."""
        return self.crud.transaction.count_all_for_period(from_date, to_date)
    
    def get_all_transaction_for_period_with_type(
        self,
        from_date: date,
        to_date: date,
        operation_type: str,
        skip: int = 0,
        limit: int = 100
    ) -> list[Transaction]:
        """
        Получить транзакции за период с фильтрацией по типу и пагинацией.
        
        Args:
            from_date: Дата начала
            to_date: Дата окончания
            operation_type: Тип операции (debit, adding, transfer)
            skip: Количество записей для пропуска
            limit: Максимальное количество записей
        
        Returns:
            Список транзакций с фильтрацией
        """
        return self.crud.transaction.get_all_transaction_for_period_with_type(
            from_date, to_date, operation_type, skip=skip, limit=limit
        )
    
    def get_total_transactions_for_period_with_type(
        self,
        from_date: date,
        to_date: date,
        operation_type: str
    ) -> int:
        """Получить общее количество транзакций за период с фильтром по типу."""
        return self.crud.transaction.count_all_for_period_with_type(
            from_date, to_date, operation_type
        )

    def check_transaction_daily_limit(self):
        """
        Проверить лимит на транзакции за день для бесплатных пользователей.
        
        Free users: max 5 transactions per day
        Paid users: no limit
        """
        if self.user_info.get('subscription_type') == 'free':
            today = date.today()
            transaction_count = (
                self.db.query(Transaction)
                .join(Transaction.transaction_distribution_user)
                .filter(
                    Transaction.transaction_distribution_user.any(
                        user_id=self.user_info.get('id'), is_deleted=False
                    ),
                    Transaction.date >= today,
                    Transaction.date <= today,
                )
                .distinct(Transaction.id)
                .count()
            )
            if transaction_count >= 5:
                raise TransactionDailyLimitError(
                    f"Бесплатные пользователи могут создавать только 5 транзакций в день. "
                    f"Вы создали {transaction_count} сегодня. Для создания дополнительных транзакций оформите подписку."
                )
    
    @commit
    def create_transaction(self, transaction_info: transaction_in):
        self.check_transaction_daily_limit()
        """
        Создать транзакцию с распределением между пользователями.

        Логика распределения:
        - owner (создатель) всегда получает распределение
        - participant — участники, переданные в distributions
        - split_type определяет, как считаются доли:
            * 'equal'   — поровну
            * 'percentage' — по процентам (из distribution.percentage)
            * 'amount'  — точные суммы (из distribution.size)
            * 'position' — по позициям (quantity * price)
        """
        # --- 1. Обновить балансы счетов ---
        self._apply_transaction_balance(transaction_info)

        # --- 2. Привязать DB-объекты ---
        db_from = (
            self.crud.account.get_by_id(transaction_info.FROM)
            if transaction_info.FROM
            else None
        )
        db_to = (
            self.crud.account.get_by_id(transaction_info.TO)
            if transaction_info.TO
            else None
        )
        db_category = (
            self.crud.category.get_by_id(transaction_info.category)
            if transaction_info.category
            else None
        )

        match transaction_info.type:
            case "debit":
                transaction_info.FROM = db_from.id if db_from else None
                transaction_info.TO = None
                transaction_info.category = db_category.id if db_category else None
            case "transfer":
                transaction_info.FROM = db_from.id if db_from else None
                transaction_info.TO = db_to.id if db_to else None
                transaction_info.category = None
                transaction_info.distributions = []
            case "adding":
                transaction_info.FROM = None
                transaction_info.TO = db_to.id if db_to else None
                transaction_info.category = db_category.id if db_category else None
                transaction_info.distributions = []

        if transaction_info.exchange_rate is None or transaction_info.exchange_rate == 0:
            if transaction_info.credit_size and transaction_info.debit_size:
                transaction_info.exchange_rate = (
                    transaction_info.credit_size / transaction_info.debit_size
                )

        # --- 3. Создать транзакцию в БД ---
        transaction = self.crud.transaction.create_transaction(transaction_info)

        # --- 4. Создать распределения ---
        self._create_distributions(transaction, transaction_info)

        return transaction

    def _apply_transaction_balance(self, transaction_info: transaction_in):
        """Применить изменения баланса к счетам."""
        if transaction_info.type == "debit":
            self.update_account_balance(
                account_in_balance(
                    id=transaction_info.FROM,
                    operation="minus",
                    balance=transaction_info.debit_size,
                ),
                commit_transaction=False,
            )
        elif transaction_info.type == "transfer":
            self.update_account_balance(
                account_in_balance(
                    id=transaction_info.FROM,
                    operation="minus",
                    balance=transaction_info.debit_size,
                ),
                commit_transaction=False,
            )
            self.update_account_balance(
                account_in_balance(
                    id=transaction_info.TO,
                    operation="plus",
                    balance=transaction_info.credit_size,
                ),
                commit_transaction=False,
            )
        elif transaction_info.type == "adding":
            self.update_account_balance(
                account_in_balance(
                    id=transaction_info.TO,
                    operation="plus",
                    balance=transaction_info.debit_size,
                ),
                commit_transaction=False,
            )

    def _create_distributions(
        self, transaction: Transaction, transaction_info: transaction_in
    ):
        """
        Создать распределения для транзакции.

        Алгоритм:
        1. Owner всегда получает распределение
        2. Участники из transaction_info.distributions
        3. Расчёт долей зависит от split_type
        """
        owner_id = self.crud.user.get_info().id
        participants = transaction_info.distributions or []
        split_type = transaction_info.split_type or 'amount'

        # Базовая сумма для распределения
        base_amount = transaction_info.debit_size

        if split_type == 'equal':
            self._distribute_equal(transaction.id, owner_id, participants, base_amount)
        elif split_type == 'percentage':
            self._distribute_by_percentage(
                transaction.id, owner_id, participants, base_amount
            )
        elif split_type == 'position':
            self._distribute_by_position(
                transaction.id, owner_id, participants, transaction_info
            )
        else:
            # 'amount' или None — используются explicit размеры
            self._distribute_by_amount(
                transaction.id, owner_id, participants, base_amount
            )

        # Создаём позиции
        if transaction_info.positions:
            for position in transaction_info.positions:
                position.transaction_id = transaction.id
                self.crud.position.create_position(position)

        # Пересчитываем статус транзакции
        self.crud.distribution.recalculate_transaction_status(transaction.id)

    def _distribute_equal(
        self,
        transaction_id: UUID,
        owner_id: UUID,
        participants: list,
        base_amount: float,
    ):
        """Распределить поровну между owner + participants."""
        total_people = 1 + len(participants)  # owner + participants
        share = round(base_amount / total_people, 2)

        # Owner
        self.crud.distribution.create_distribution(
            distribution_in(
                user_id=owner_id,
                transaction_id=transaction_id,
                role='owner',
                size=share,
            )
        )

        # Participants
        for p in participants:
            self.crud.distribution.create_distribution(
                distribution_in(
                    user_id=p.user_id,
                    transaction_id=transaction_id,
                    role='participant',
                    size=share,
                )
            )

        # Корректируем остаток на owner (из-за округления)
        distributed = self.crud.distribution.get_total_distributed(transaction_id)
        remainder = round(base_amount - distributed, 2)
        if remainder != 0:
            owner_distr = self.crud.distribution.get_distribution(
                transaction_id, owner_id
            )
            owner_distr.size = round(owner_distr.size + remainder, 2)

    def _distribute_by_percentage(
        self,
        transaction_id: UUID,
        owner_id: UUID,
        participants: list,
        base_amount: float,
    ):
        """
        Распределить по процентам.
        percentage в distribution — доля участника (0.0–1.0).
        Остаток идёт owner'у.
        """
        participant_total_pct = sum(
            (p.percentage or 0) for p in participants if p.percentage
        )
        owner_pct = max(0, 1.0 - participant_total_pct)

        # Owner
        self.crud.distribution.create_distribution(
            distribution_in(
                user_id=owner_id,
                transaction_id=transaction_id,
                role='owner',
                size=round(base_amount * owner_pct, 2),
            )
        )

        # Participants
        for p in participants:
            pct = p.percentage if p.percentage is not None else 0
            self.crud.distribution.create_distribution(
                distribution_in(
                    user_id=p.user_id,
                    transaction_id=transaction_id,
                    role='participant',
                    size=round(base_amount * pct, 2),
                )
            )

        # Корректируем остаток на owner
        distributed = self.crud.distribution.get_total_distributed(transaction_id)
        remainder = round(base_amount - distributed, 2)
        if remainder != 0:
            owner_distr = self.crud.distribution.get_distribution(
                transaction_id, owner_id
            )
            owner_distr.size = round(owner_distr.size + remainder, 2)

    def _distribute_by_amount(
        self,
        transaction_id: UUID,
        owner_id: UUID,
        participants: list,
        base_amount: float,
    ):
        """
        Распределить по точным суммам.
        size в distribution — конкретная сумма участника.
        Остаток идёт owner'у.
        """
        participant_total = sum(
            (p.size or 0) for p in participants if p.size is not None
        )
        owner_share = round(base_amount - participant_total, 2)

        # Owner получает остаток
        self.crud.distribution.create_distribution(
            distribution_in(
                user_id=owner_id,
                transaction_id=transaction_id,
                role='owner',
                size=owner_share,
            )
        )

        # Participants
        for p in participants:
            self.crud.distribution.create_distribution(
                distribution_in(
                    user_id=p.user_id,
                    transaction_id=transaction_id,
                    role='participant',
                    size=p.size if p.size is not None else 0,
                )
            )

    def _distribute_by_position(
        self,
        transaction_id: UUID,
        owner_id: UUID,
        participants: list,
        transaction_info: transaction_in,
    ):
        """
        Распределить по позициям.
        Каждая позиция — это товар/услуга с price и quantity.
        Сумма позиции = price * quantity.
        """
        if not transaction_info.positions:
            # Fallback на equal, если позиций нет
            self._distribute_equal(
                transaction_id, owner_id, participants, transaction_info.debit_size
            )
            return

        total_position_value = sum(
            p.price * p.quantity for p in transaction_info.positions
        )

        if total_position_value == 0:
            self._distribute_equal(
                transaction_id, owner_id, participants, transaction_info.debit_size
            )
            return

        # Owner получает всё, если нет участников
        if not participants:
            self.crud.distribution.create_distribution(
                distribution_in(
                    user_id=owner_id,
                    transaction_id=transaction_id,
                    role='owner',
                    size=transaction_info.debit_size,
                )
            )
            return

        # Распределяем стоимость позиций поровну
        total_people = 1 + len(participants)
        share = round(transaction_info.debit_size / total_people, 2)

        self.crud.distribution.create_distribution(
            distribution_in(
                user_id=owner_id,
                transaction_id=transaction_id,
                role='owner',
                size=share,
            )
        )

        for p in participants:
            self.crud.distribution.create_distribution(
                distribution_in(
                    user_id=p.user_id,
                    transaction_id=transaction_id,
                    role='participant',
                    size=share,
                )
            )

        # Корректируем остаток
        distributed = self.crud.distribution.get_total_distributed(transaction_id)
        remainder = round(transaction_info.debit_size - distributed, 2)
        if remainder != 0:
            owner_distr = self.crud.distribution.get_distribution(
                transaction_id, owner_id
            )
            owner_distr.size = round(owner_distr.size + remainder, 2)

    # ------------------------------------------------------------------ #
    #              Transaction updates & delete                           #
    # ------------------------------------------------------------------ #

    @commit
    def update_transaction_date(self, transaction_info: transaction_in_date):
        return self.crud.transaction.update_date(transaction_info)

    @commit
    def update_transaction_size(self, transaction_info: transaction_in_size):
        transaction = self.crud.transaction.update_size(transaction_info)
        if transaction:
            # При изменении размера пересчитываем распределения пропорционально
            self._rescale_distributions(transaction.id, transaction.debit_size)
        return transaction

    def _rescale_distributions(self, transaction_id: UUID, new_debit_size: float):
        """Пересчитать размеры распределений пропорционально новому размеру."""
        distributions = self.crud.distribution.get_distributions_for_transaction(
            transaction_id
        )
        old_total = sum(d.size for d in distributions if d.size)
        if old_total == 0:
            return
        for distr in distributions:
            if distr.size:
                distr.size = round(distr.size / old_total * new_debit_size, 2)

    @commit
    def update_transaction_description(self, transaction_info: transaction_in_description):
        return self.crud.transaction.update_description(transaction_info)

    @commit
    def delete_transaction(self, id: UUID) -> Transaction:
        """
        Удалить транзакцию:
        1. Получить транзакцию
        2. Soft-delete все распределения
        3. Вернуть балансы счетов
        4. Удалить транзакцию
        """
        transaction = self.crud.transaction.get_by_id(id)
        if transaction is None:
            raise TransactionNotFoundError(f"Транзакция {id} не найдена")

        # Soft-delete распределений
        self.crud.distribution.delete_all_distributions(id)

        # Вернуть балансы
        self._reverse_transaction_balance(transaction)

        # Удалить транзакцию
        return self.crud.transaction.delete(id)

    def _reverse_transaction_balance(self, transaction: Transaction):
        """Отменить изменения баланса при удалении транзакции."""
        if transaction.type == "debit":
            if transaction.from_account_id:
                self.update_account_balance(
                    account_in_balance(
                        id=transaction.from_account_id,
                        operation="plus",
                        balance=transaction.debit_size,
                    ),
                    commit_transaction=False,
                )
        elif transaction.type == "transfer":
            if transaction.from_account_id:
                self.update_account_balance(
                    account_in_balance(
                        id=transaction.from_account_id,
                        operation="plus",
                        balance=transaction.debit_size,
                    ),
                    commit_transaction=False,
                )
            if transaction.to_account_id:
                self.update_account_balance(
                    account_in_balance(
                        id=transaction.to_account_id,
                        operation="minus",
                        balance=transaction.credit_size,
                    ),
                    commit_transaction=False,
                )
        elif transaction.type == "adding":
            if transaction.to_account_id:
                self.update_account_balance(
                    account_in_balance(
                        id=transaction.to_account_id,
                        operation="minus",
                        balance=transaction.credit_size or transaction.debit_size,
                    ),
                    commit_transaction=False,
                )

    # ------------------------------------------------------------------ #
    #              Distribution operations                                #
    # ------------------------------------------------------------------ #

    @commit
    def transaction_add_distribution(self, distribution_info: distribution_in):
        transaction = self.crud.transaction.get_by_id(distribution_info.transaction_id)
        if transaction is None:
            raise TransactionNotFoundError(
                f"Транзакция {distribution_info.transaction_id} не найдена"
            )
        result = self.crud.distribution.create_distribution(distribution_info)
        self.crud.distribution.recalculate_transaction_status(
            distribution_info.transaction_id
        )
        return result

    @commit
    def transaction_update_distribution(self, distribution_info: distribution_in):
        result = self.crud.distribution.update_distribution(distribution_info)
        self.crud.distribution.recalculate_transaction_status(
            distribution_info.transaction_id
        )
        return result

    @commit
    def transaction_delete_distribution(self, distribution_info: distribution_in):
        result = self.crud.distribution.delete_distribution(distribution_info)
        self.crud.distribution.recalculate_transaction_status(
            distribution_info.transaction_id
        )
        return result

    @commit
    def transaction_settle_distribution(self, settle_info: distribution_settle_in):
        """Пометить распределение как оплаченное."""
        result = self.crud.distribution.settle_distribution(settle_info)
        self.crud.distribution.recalculate_transaction_status(
            settle_info.transaction_id
        )
        return result

    # ------------------------------------------------------------------ #
    #              Position operations                                    #
    # ------------------------------------------------------------------ #

    @commit
    def transaction_add_position(self, position_info: position_in):
        return self.crud.position.create_position(position_info)

    @commit
    def transaction_update_position(self, position_info: position_in):
        return self.crud.position.update_position(
            position_info.transaction_id, position_info
        )
