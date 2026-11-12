from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.category import Category
from app.repository.category import CategoryRepo
from app.schemas.category import CategoryCreate, CategoryUpdate

class CategoryService:
    def __init__(self, db:Session):
        self.repo = CategoryRepo(db)
        
    def get_or_404(self, category_id:int)->Category:
        category = self.repo.get(category_id)
        if category is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=f"Category {category_id} not found")
        return category

    def list(self) -> list[Category]:
        return self.repo.list()
    
    def create(self, data: CategoryCreate) ->Category:
        if self.repo.get_by_name(data.name):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail=f"Category with name '{data.name}' already exists")
        return self.repo.create(data)
    
    def update(self, category_id: int, data: CategoryUpdate) -> Category:
        category = self.get_or_404(category_id)
        # если меняется имя — проверяем уникальность
        if data.name and data.name != category.name:
            if self.repo.get_by_name(data.name):
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=f"Category with name '{data.name}' already exists",
                )
        return self.repo.update(category, data)
