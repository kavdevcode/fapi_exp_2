from sqlalchemy.orm import Session
from app.models import Category
from app.schemas import CategoryCreate, CategoryUpdate


class CategoryRepo:
    def __init__(self, db:Session):
        self.db = db
        
    def get(self, category_id:int) -> Category|None:
        return self.db.get(Category, category_id)
      
    def list(self)->list[Category]:
        return self.db.query(Category).all()
    
    def create(self, data:CategoryCreate)->Category:
        category = Category(**data.model_dump())
        self.db.add(category)
        self.db.commit()
        self.db.refresh(category)
        return category
    
    def get_by_name(self, name: str) -> Category|None:
        return self.db.query(Category).filter(Category.name == name).first() 
        
    def update(self, category: Category, data:CategoryUpdate)->Category:
        for field, value in data.model_dump(exclude_unset=True).items():
           setattr(category,field,value)
        self.db.commit()
        self.db.refresh(category)
        return category 
            
    def delete(self, category: Category) -> None:
        self.db.delete(category)
        self.db.commit()