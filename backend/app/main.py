from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.logger import setup_logging, logger
from app.api.health import router as health_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_logging()
    logger.info(
        "Starting Offline Agentic AI Backend",
        project=settings.PROJECT_NAME,
        environment=settings.ENVIRONMENT,
    )
    yield
    logger.info("Shutting down Offline Agentic AI Backend")


app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Offline Agentic AI for Financial Fraud Detection & Investigation",
    version="0.1.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router, tags=["Health"])


@app.get("/")
async def root():
    return {
        "message": "Welcome to Offline Agentic AI Platform API",
        "docs": "/docs",
        "health": "/health",
    }
