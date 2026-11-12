from pydantic import BaseModel, ConfigDict, Field


class ProductBase(BaseModel):
    name: str = Field(..., min_length=3, max_length=100)
    price: float = Field(..., ge=0)
    
    
class ProductCreate(ProductBase):
    category_id: int
    

class ProductUpdate(BaseModel):
    name: str = Field(..., min_length=3, max_length=100)
    price: float = Field(..., ge=0)
    category_id: int
    
class ProductRead(ProductBase):
    id: int
    category_id: int
    model_config = ConfigDict(from_attributes=True)
    

