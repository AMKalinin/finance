from uuid import UUID

from app.crud.crud_base import CRUD_base
from app.models.category import Category
from app.schemas.category import category_in, category_in_name


class CRUD_category(CRUD_base):
    def get_all(self) -> list[Category]: 
        return self.user.categories.filter(
                Category.is_deleted == False).all() 
    
    def get_all_structured_list(self) -> list[Category]:
        return self.user.categories.filter(
                Category.level == 1).filter(
                Category.is_deleted == False).all()

    #def get_all_flat_list(self)-> list[Category]:
    #    return self.user.categories.filter


    def get_by_id(self, id: UUID) -> Category:
        return self.user.categories.filter(
            Category.id == id
        ).first()  

    def create_category(self, category_info: category_in) -> Category:
        db_category = Category(
            name=category_info.name,
            type_category=category_info.type_category,
            user_id=self.user.id,
            parent_id=category_info.parent_category,
            level=category_info.level
        )  # type: ignore
        self.db.add(db_category)
        return db_category

    def delete_category(self, id: UUID) -> Category:
        db_category = self.user.categories.filter(
            Category.id == id
        ).first()  
        
        if db_category == None:
            return db_category
        
        for sub_cat in db_category.children:
            self.delete_category(sub_cat.id)

        db_category.is_deleted = True
        db_category.old_parent_id = db_category.parent_id 
        db_category.parent_id = None
        return db_category

    def update_name(self, category_info: category_in_name) -> Category | None:
        db_category = self.user.categories.filter(Category.id == category_info.id).first()

        if db_category == None:
            return db_category

        db_category.name = category_info.name
        return db_category


# category = CRUD_category()
