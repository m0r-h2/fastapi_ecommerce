from uuid import uuid4
from fastapi.responses import JSONResponse
from fastapi import Request
from loguru import logger
from app.core.config import settings

logger.add(
    "info.log",
    format=settings.logging.format,
    level=settings.logging.log_lvl,
    enqueue=True,
)


async def log_middleware(request: Request, call_next):
    log_id = str(uuid4())
    with logger.contextualize(log_id=log_id):
        try:
            response = await call_next(request)
            if response.status_code in [401, 402, 403, 404]:
                logger.warning(f"Request to {request.url.path}")
            else:
                logger.info("Successfully accessed " + request.url.path)
        except Exception as ex:
            logger.error(f"Request to {request.url.path} failed: {ex}")
            response = JSONResponse(content={"success": False}, status_code=500)
        return response
