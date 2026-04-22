from uuid import UUID

from app.crud.crud_base import CRUD_base
from app.models.position import Position

from app.schemas.position import position_in


class CRUD_position(CRUD_base):
    def create_position(self, position:position_in) -> Position:
        db_position = Position(
                    name=position.name,
                    transaction_id=position.transaction_id,
                    price=position.price,
                    quantity=position.quantity
                )
        self.db.add(db_position)
        return db_position

    def update_position(self, id:UUID, position_info:position_in) -> Position:
        db_position = self.db.query(Position).get(id)
        db_position.price = position_info.price
        db_position.quantity = position_info.quantity
        return db_position 

    def get_positions(self, transaction_id:UUID) -> list[Position]:
        res = [
            position 
            for position in self.user.transaction_distribution_user
            if position.transaction_id == transaction_id
        ]
        return res

