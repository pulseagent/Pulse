import os

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.status import HTTP_403_FORBIDDEN

API_KEY_NAME = "X-API-Key"
API_KEY = os.getenv("API_KEY")

class APIKeyMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next):
        api_key = request.headers.get(API_KEY_NAME)
        if api_key != API_KEY:
            return JSONResponse(
                status_code=HTTP_403_FORBIDDEN,
                content={"detail": "Could not validate API Key"},
            )
        response = await call_next(request)
        return response