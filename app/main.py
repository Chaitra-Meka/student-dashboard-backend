from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.database import Base, engine
from app import models  # Registers the Student model with SQLAlchemy
from app.routers.students import router as students_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title=settings.app_name,
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(students_router)


@app.get("/api/health", tags=["Health"])
def health_check():
    return {"status": "ok", "message": "Student Dashboard API is running"}