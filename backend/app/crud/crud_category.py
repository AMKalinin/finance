from uuid import UUID

from app.crud.crud_base import CRUD_base
from app.models.category import Category
from app.schemas.category import category_in, category_in_name


class CRUD_category(CRUD_base):
    def get_all(self, skip: int = 0, limit: int = 100) -> list[Category]: 
        """
        Получить все категории с пагинацией.
        
        Args:
            skip: Количество записей для пропуска
            limit: Максимальное количество записей
        
        Returns:
            Список категорий
        """
        return (
            self.user.categories
            .filter(Category.is_deleted == False)
            .offset(skip)
            .limit(limit)
            .all()
        )
    
    def count_all(self) -> int:
        """Получить общее количество активных категорий."""
        return self.user.categories.filter(
            Category.is_deleted == False
        ).count()
    
    def get_all_structured_list(self, skip: int = 0, limit: int = 100) -> list[Category]:
        """
        Получить корневые категории (уровень 1) с пагинацией.
        
        Args:
            skip: Количество записей для пропуска
            limit: Максимальное количество записей
        
        Returns:
            Список корневых категорий со вложенными подкатегориями
        """
        return (
            self.user.categories
            .filter(Category.level == 1, Category.is_deleted == False)
            .offset(skip)
            .limit(limit)
            .all()
        )
    
    def get_by_type(self, category_type: str, skip: int = 0, limit: int = 100) -> list[Category]:
        """
        Получить категории по типу с пагинацией.
        
        Args:
            category_type: Тип категории (expense, income)
            skip: Количество записей для пропуска
            limit: Максимальное количество записей
        
        Returns:
            Список категорий указанного типа
        """
        return (
            self.user.categories
            .filter(
                Category.is_deleted == False,
                Category.type == category_type
            )
            .offset(skip)
            .limit(limit)
            .all()
        )
    
    def count_by_type(self, category_type: str) -> int:
        """Получить общее количество категорий указанного типа."""
        return self.user.categories.filter(
            Category.is_deleted == False,
            Category.type == category_type
        ).count()

    #def get_all_flat_list(self)-> list[Category]:
    #    return self.user.categories.filter


    def get_by_id(self, id: UUID) -> Category:
        return self.user.categories.filter(
            Category.id == id
        ).first()  

    def create_category(self, category_info: category_in) -> Category:
        db_category = Category(
            name=category_info.name,
            type=category_info.type,
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
