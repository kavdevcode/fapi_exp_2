from pydantic import BaseModel, ConfigDict, Field
from .product import ProductRead

class CategoryBase(BaseModel):
    name: str = Field(..., min_length=5, max_length=100)
    description: str|None = None
    
class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(BaseModel):
    name: str | None = Field(None, min_length=5, max_length=100)
    description: str |None = None


class CategoryRead(CategoryBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

class CategoryWithProducts(CategoryRead):
    products: list[ProductRead] = []