from uuid import UUID

from app.crud.crud_base import CRUD_base
from app.models.transaction_distribution_user import Transaction_distribution_user

from app.schemas.distribution import distribution_in


class CRUD_distribution(CRUD_base):
    def create_distribution(self, distribution: distribution_in) -> Transaction_distribution_user:
        db_distr = Transaction_distribution_user(
            user_id=distribution.user_id,
            transaction_id=distribution.transaction_id,
            distribution_user_role=distribution.role,
            size=distribution.size,
            distribution_status='settled'
        )
        self.db.add(db_distr)
        return db_distr

    def get_distribution(self, transaction_id:UUID) -> Transaction_distribution_user:
        res = [
            distr
            for distr in self.user.transaction_distribution_user
            if  distr.transaction_id == transaction_id
        ]
        return res[0]
 
    def update_distribution(self, distribution_info:distribution_in) -> Transaction_distribution_user:
        db_distr = self.db.query(Transaction_distribution_user).get((distribution_info.user_id, distribution_info.transaction_id))
        if distribution_info.size:
            db_distr.size = distribution_info.size
        return db_distr
 
    def delete_distribution(self, distribution_info:distribution_in) -> None:
        db_distr = self.db.query(Transaction_distribution_user).get((distribution_info.user_id, distribution_info.transaction_id))
        self.db.delete(db_distr)
 

