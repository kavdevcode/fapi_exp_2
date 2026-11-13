from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.product import Product
from app.repository.category import CategoryRepo
from app.repository.product import ProductRepo
from app.schemas.product import ProductCreate, ProductUpdate


class ProductService:
    def __init__(self, db:Session):
        self.repo = ProductRepo(db)
        self.category_repo = CategoryRepo(db)
        
    
    def get_or_404(self, product_id:int)->Product|None:
        product = self.repo.get(product_id)
        if product is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="not found product"
            )
        return product
    
    def list(self, category_id:int)->list[Product]:
        return self.repo.list(category_id)
    
    def _ensure_category_exists(self, category_id: int) -> None:
        if self.category_repo.get(category_id) is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Category {category_id} does not exist",
            )

    def create(self, data: ProductCreate) -> Product:
        self._ensure_category_exists(data.category_id)
        return self.repo.create(data)

    def update(self, product_id: int, data: ProductUpdate) -> Product:
        product = self.get_or_404(product_id)
        if data.category_id is not None:
            self._ensure_category_exists(data.category_id)
        return self.repo.update(product, data)

    def delete(self, product_id: int) -> None:
        product = self.get_or_404(product_id)
        self.repo.delete(product)
