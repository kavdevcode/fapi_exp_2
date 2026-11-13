from sqlalchemy.orm import Session
from app.models import Product
from app.schemas.product import ProductCreate, ProductUpdate


class ProductRepo:
    def __init__(self, db:Session):
        self.db = db
    
    def get(self, product_id: int) ->Product|None:
        return self.db.get(Product, product_id)
    
    def list(self, category_id:int|None=None) ->list[Product]:
        query = self.db.query(Product)
        if category_id is not None:
            query = query.filter(Product.category_id == category_id )
        return query.all()
    
    def create(self, data:ProductCreate) -> Product:
        product = Product(**data.model_dump())
        self.db.add(product)
        self.db.commit()
        self.db.refresh(product)
        return product
    
    def update(self, product: Product, data:ProductUpdate)->Product:
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(product, field, value)
        self.db.commit()
        self.db.refresh(product)
        return product
    
    def delete(self, product: Product)->None:
        self.db.delete(product)
        self.db.commit()
        
