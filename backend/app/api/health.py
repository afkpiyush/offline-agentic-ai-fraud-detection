from fastapi import APIRouter, Response, status
import asyncpg
import redis.asyncio as aioredis
import httpx
from app.config import settings
from app.logger import logger

router = APIRouter()


@router.get("/health")
async def health_check(response: Response):
    services_status = {}
    overall_healthy = True

    # 1. Check PostgreSQL
    try:
        conn = await asyncpg.connect(
            user=settings.POSTGRES_USER,
            password=settings.POSTGRES_PASSWORD,
            database=settings.POSTGRES_DB,
            host=settings.POSTGRES_HOST,
            port=settings.POSTGRES_PORT,
            timeout=3.0,
        )
        await conn.execute("SELECT 1")
        await conn.close()
        services_status["postgres"] = "connected"
    except Exception as e:
        logger.error("Health check failed for PostgreSQL", error=str(e))
        services_status["postgres"] = f"unreachable: {str(e)}"
        overall_healthy = False

    # 2. Check Redis
    try:
        r = aioredis.from_url(settings.redis_url, socket_timeout=3.0)
        await r.ping()
        await r.aclose()
        services_status["redis"] = "connected"
    except Exception as e:
        logger.error("Health check failed for Redis", error=str(e))
        services_status["redis"] = f"unreachable: {str(e)}"
        overall_healthy = False

    # 3. Check Ollama
    try:
        async with httpx.AsyncClient(timeout=3.0) as client:
            res = await client.get(f"{settings.OLLAMA_BASE_URL}/api/tags")
            if res.status_code == 200:
                services_status["ollama"] = "connected"
            else:
                services_status["ollama"] = f"error: status code {res.status_code}"
                overall_healthy = False
    except Exception as e:
        logger.error("Health check failed for Ollama", error=str(e))
        services_status["ollama"] = f"unreachable: {str(e)}"
        overall_healthy = False

    if not overall_healthy:
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE

    return {
        "status": "healthy" if overall_healthy else "unhealthy",
        "environment": settings.ENVIRONMENT,
        "services": services_status,
    }
