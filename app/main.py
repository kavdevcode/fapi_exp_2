from fastapi import FastAPI
from .config import settings

from .database import Base, engine


Base.metadata.create_all(bind=engine)
app = FastAPI(title=settings.app_name, debug=settings.debug)


@app.get("/")
def root():
    return {"app": settings.app_name, "status": "ok"}
