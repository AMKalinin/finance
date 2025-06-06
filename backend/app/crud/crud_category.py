from uuid import UUID

from app.crud.crud_base import CRUD_base
from app.models.category import Category
from app.schemas.category import category_in, category_in_name


class CRUD_category(CRUD_base):
    def get_all(self) -> list[Category]:
        return self.user.categories.all()  # self.db.query(Category).all()

    def get_by_id(self, id: UUID) -> Category:
        return self.user.categories.filter(
            Category.id == id
        ).first()  # self.db.query(Category).get(id)

    def create_category(self, category_info: category_in) -> Category:
        db_category = Category(
            name=category_info.name, type_category=category_info.type_category, user_id=self.user.id
        )  # type: ignore
        self.db.add(db_category)
        return db_category

    def delete_category(self):
        pass

    def update_name(self, category_info: category_in_name) -> Category | None:
        db_category = self.user.categories.filter(Category.id == category_info.id).first()

        if db_category == None:
            return db_category

        db_category.name = category_info.name
        # db.commit()
        return db_category


# category = CRUD_category()
