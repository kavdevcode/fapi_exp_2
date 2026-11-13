from fastapi import FastAPI
from .config import settings
from app.routers import category as category_router
from app.routers import product as product_router
from .database import Base, engine


Base.metadata.create_all(bind=engine)
app = FastAPI(title=settings.app_name, debug=settings.debug)

app.include_router(category_router.router)
app.include_router(product_router.router)

@app.get("/")
def root():
    return {"app": settings.app_name, "status": "ok"}
