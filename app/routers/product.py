from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.product import ProductCreate, ProductRead, ProductUpdate
from app.services.product import ProductService


router = APIRouter(prefix="/products", tags=["products"])

def get_service(db:Session = Depends(get_db)) -> ProductService:
    return ProductService(db)


@router.get("/", response_model=list[ProductRead])
def list_products(
    category_id: int| None = Query(None, description="Фильтр по категории"),
    service: ProductService = Depends(get_service)
):
    return service.list(category_id)


@router.get("/{product_id}", response_model=ProductRead)
def get_product(product_id: int, service: ProductService = Depends(get_service)):
    return service.get_or_404(product_id)


@router.post("/", response_model=ProductRead, status_code=status.HTTP_201_CREATED)
def create_product(
    payload: ProductCreate,
    service: ProductService = Depends(get_service),
):
    return service.create(payload)


@router.patch("/{product_id}", response_model=ProductRead)
def update_product(
    product_id: int,
    payload: ProductUpdate,
    service: ProductService = Depends(get_service),
):
    return service.update(product_id, payload)
