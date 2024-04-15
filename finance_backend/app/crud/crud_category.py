from sqlalchemy.orm import Session

from app.models.category import Category
from app.schemas.category import category_in, category_in_name


class CRUD_category:
    def get_all(self, db: Session) -> list[Category]:
        return db.query(Category).all()

    def create_category(self, db: Session, category_info: category_in) -> Category:
        db_category = Category(
            name=category_info.name, type_name=category_info.type_name
        )  # type: ignore
        db.add(db_category)
        db.commit()
        db.refresh(db_category)
        return db_category

    def delete_category(self):
        pass

    def update_name(self, db: Session, category_info: category_in_name) -> Category:
        db_category = db.query(Category).get(category_info.id)
        db_category.name = category_info.name
        db.commit()
        return db_category


category = CRUD_category()
