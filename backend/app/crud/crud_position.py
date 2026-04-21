from uuid import UUID

from app.crud.crud_base import CRUD_base
from app.models.position import Position

from app.schemas.position import (position_in)


class CRUD_position(CRUD_base):
    def create_position(self, position_info:position_in) -> Position:
        db_position = Position(
            name=position_info.name,
            transaction_id=position_info.transaction_id,
            price=position_info.price,
            quantity=position.quantity 
        )
        self.db.add(db_position)
        return db_position
