from sqlalchemy.orm import Session  # noqa

from app.models.account import Account 
from app.models.category import Category, Category_type 
from app.models.transaction import Transaction, Transaction_type, Transaction_status, Split_type  
from app.models.user import User, Subscription_type
from app.models.friends import  Friends , Friends_status
from app.models.transaction_distribution_user import Transaction_distribution_user, Distribution_status, Distribution_user_role
from app.models.position import Position
from app.models.position_user import Position_user

from .base_class import Base
from .session import engine


def init_db():
    Base.metadata.create_all(engine)  # type: ignore
    with Session(engine) as session:
        with session.begin():
            type_debit = (
                session.query(Transaction_type).filter(Transaction_type.name == "debit").first()
            )
            if type_debit:
                return 

            type_c_debit = Category_type(
                name="debit", description="Debit / списание"
            )  # type: ignore
            session.add(type_c_debit)

            type_c_adding = Category_type(
                name="adding", description="Adding / пополнение"
            )  # type: ignore
            session.add(type_c_adding)



            type_debit = Transaction_type(
                name="debit", description="Debit / списание"
            )  # type: ignore
            session.add(type_debit)

            type_transfer = Transaction_type(
                name="transfer", description="Transfer / перевод"
            )  # type: ignore
            session.add(type_transfer)

            type_adding = Transaction_type(
                name="adding", description="Adding / пополнение"
            )  # type: ignore
            session.add(type_adding)


            transaction_status_pending = Transaction_status(
                    name='pending', description='Ожидание'
                    )
            session.add(transaction_status_pending)
            transaction_status_partially_paid = Transaction_status(
                    name='partially_paid', description='Транзакция частично закрыта'
                    )
            session.add(transaction_status_partially_paid)
            transaction_status_settled = Transaction_status(
                    name='settled', description='Транзаеция завершена'
                    )
            session.add(transaction_status_settled)


            split_type_equal = Split_type(
                    name='equal', description='Поровну'
                    )
            session.add(split_type_equal)
            split_type_percentage = Split_type(
                    name='percentage', description='Проценты'
                    )
            session.add(split_type_percentage)
            split_type_amount = Split_type(
                    name='amount', description='Конкретные суммы'
                    )
            session.add(split_type_amount)
            split_type_position = Split_type(
                    name='position', description='По позициям'
                    )
            session.add(split_type_position)


            distribution_status_pending = Distribution_status(
                    name='pending', description='Ожидание'
                    )
            session.add(distribution_status_pending )
            distribution_status_settled = Distribution_status(
                    name='settled', description='Распределение завершено'
                    )
            session.add(distribution_status_settled)


            subscription_type_free = Subscription_type(
                    name='free', description='Бесплатный тип подписки'
                    )
            session.add(subscription_type_free)
            subscription_type_premium = Subscription_type(
                    name='premium', description='Премиум тип подписки'
                    )
            session.add(subscription_type_premium)


            friends_status_pending_sent = Friends_status(
                    name="pending_sent", description="Отправитель ожидает ответ"
                    )
            session.add(friends_status_pending_sent)
            friends_status_accepted = Friends_status(
                    name="accept", description="Подтверждённая дружба"
                    )
            session.add(friends_status_accepted)
            friends_status_pending_received = Friends_status(
                    name="pending_received", description="Ожидание ответа от получателя"
                    )
            session.add(friends_status_pending_received)
