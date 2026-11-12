from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.category import CategoryRead, CategoryCreate, CategoryUpdate, CategoryWithProducts
from app.services.category import CategoryService

router = APIRouter(prefix="/category", tags=["categories"])

def get_service(db: Session = Depends(get_db)):
    return CategoryService(db)


@router.get("/{category_id}", response_model=CategoryWithProducts)
def get_category(category_id:int, service: CategoryService = Depends(get_service)):
    return service.get_or_404(category_id)

@router.get("/", response_model=list[CategoryRead])
def list_categories(service: CategoryService = Depends(get_service)):
    return service.list()

@router.post("/", response_model=CategoryRead, status_code=status.HTTP_201_CREATED)
def create_category(payload: CategoryCreate, service: CategoryService = Depends(get_service)):
    return service.create(payload)


@router.patch("/{category_id}", response_model=CategoryRead)
def update_category(
    category_id: int,
    payload: CategoryUpdate,
    service: CategoryService = Depends(get_service),
):
    return service.update(category_id, payload)
