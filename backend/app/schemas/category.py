from uuid import UUID
from pydantic import BaseModel, Field, ConfigDict


class category_in(BaseModel):
    name: str
    type: str = Field(default=None)
    parent_category: UUID | None = Field(alias="parentCategory", default=None)
    level: int | None = 1


class category_in_name(BaseModel):
    id: UUID
    name: str


def serialize_children(children_list, depth=0):
    """Рекурсивно сериализует вложенные категории."""
    result = []
    for child in children_list or []:
        if isinstance(child, CategorySchema):
            result.append(serialize_category(child))
        elif hasattr(child, 'id'):
            # Это SQLAlchemy модель Category
            serialized = {
                'id': str(child.id),
                'name': child.name,
                'type': child.type,
                'level': child.level,
                'children': serialize_children(child.children, depth + 1)
            }
            result.append(serialized)
    return result


def serialize_category(category):
    """Сериализует одну категорию с детьми."""
    if isinstance(category, CategorySchema):
        return {
            **category.model_dump(),
            'subCategory': category.children or []
        }

    # Это SQLAlchemy модель Category
    return {
        'id': str(category.id),
        'name': category.name,
        'type': category.type,
        'level': category.level,
        'children': serialize_children(category.children)
    }


class CategorySchema(BaseModel):
    id: UUID
    name: str
    type: str
    level: int
    children: list['CategorySchema'] = Field(default=[], serialization_alias="subCategory")
    model_config = ConfigDict(from_attributes=True, extra='ignore')


category_out = CategorySchema
