import json
import logging
from datetime import datetime
from functools import wraps
from typing import Type

from aiofauna import Api, ApiClient
from aiofauna.api import Handler
from aiohttp.web import Request, Response, json_response, middleware
from aiohttp.web_exceptions import (HTTPException, HTTPNotFound,
                                    HTTPUnauthorized)
from rich.logging import RichHandler

from .config import env
from .schemas.models import User


class JsonFormatter(logging.Formatter):
    def format(self, record):
        record_dict = {
            'timestamp': record.created,
            'level': record.levelname,
            'message': record.getMessage(),
            'module': record.module,
            'line': record.lineno,
            'function': record.funcName,
            'exception': record.exc_info,
        }
        return json.dumps(record_dict)

file_handler = logging.FileHandler(f'logs/{datetime.now().strftime("%Y-%m-%d")}.log')
file_handler.setFormatter(JsonFormatter())

logging.basicConfig(
    level=logging.DEBUG,
    format="%(message)s",
    datefmt="[%X]",
    handlers=[
        RichHandler(rich_tracebacks=True), 
        file_handler
    ],
)

logger = logging.getLogger('rich')


client = ApiClient()


def middlewares(self: Api):
    @self.middleware
    async def general_error_middleware(request: Request, handler: Handler):
        """Handles errors"""
        try:
            return await handler(request)
        except Exception as exception:
            logger.error(f"Unexpected error: {exception.__class__.__name__}")
            logger.error(f"Error: {exception}")
            return json_response(
                {"message": "Unexpected server error", "status": "error"}, status=500
            )

    @self.middleware
    async def http_error_middleware(request: Request, handler: Handler):
        """Handles errors"""
        try:
            return await handler(request)
        except HTTPException as exception:
            if exception.status < 500:
                logger.warning(
                    f"{request.remote} tried to access {request.path} without success - Http error {exception.status} - Message: {exception.text}"
                )
                return json_response(
                    {"message": f"Error {exception.status}", "status": "error"},
                    status=exception.status,
                )
            return json_response(
                {"message": "Unexpected network error", "status": "error"}, status=500
            )

    @self.middleware
    async def auth_middleware(request: Request, handler: Handler):
        """Authenticates a user"""
        try:
            if request.path.startswith("/api"):
                authorization = request.headers.get("Authorization")
                if authorization is None:
                    return await handler(request)
                token = authorization.split(" ")[1]
                request.token = token # type: ignore
                return await handler(request)
            return await handler(request)
        except HTTPUnauthorized as exception:
            logger.warning(
                f"The {request.remote} address tried to access {request.path} without authorization"
            )
            return json_response(
                {"message": str(exception), "status": "error"}, status=401
            )

    @self.middleware
    async def notfound_middleware(request: Request, handler: Handler):
        """Redirects to Api root on 404"""
        try:
            return await handler(request)
        except HTTPNotFound as exception:
            logger.warning(
                f"The {request.remote} address requested {request.path} without success"
            )
            return json_response(
                {"message": str(exception), "status": "warning"}, status=404
            )

    @self.get("/api/auth")
    async def auth(request: Request):
        """Auth0 login"""
        token = request.token # type: ignore
        assert isinstance(token, str)
        data = await client.fetch(
                    f"{env.AUTH0_URL}/userinfo", "GET",
                    headers={"Authorization": f"Bearer {token}"},
                )
        assert isinstance(data, dict)
        return await User(**data).save()
    
    return self


def middleware_stack():
    """Middleware Injector"""

    def decorator(cls: Type[Api]):
        @wraps(cls)
        def wrapper(*args, **kwargs):
            return middlewares(cls(*args, **kwargs))

        return wrapper

    return decorator


def auth():
    @middleware
    async def _token_required(request: Request, handler: Handler):
        # Extract token from header
        authorization = request.headers.get("Authorization", None)
        if not authorization:
            raise HTTPUnauthorized(
                reason="Token missing in header",
                body=json_response(
                    {"message": "Token missing in header", "status": "error"},
                    status=401,
                ),
            )

        # Extract token from bearer
        parts = authorization.split()
        if parts[0].lower() != "bearer":
            raise HTTPUnauthorized(
                reason='Invalid token header. No "bearer" keyword',
                body=json_response(
                    {
                        "message": "Invalid token header. No 'bearer' keyword",
                        "status": "error",
                    },
                    status=401,
                ),
            )
        elif len(parts) == 1:
            raise HTTPUnauthorized(
                reason="Invalid token header. No credentials provided",
                body=json_response(
                    {
                        "message": "Invalid token header. No credentials provided",
                        "status": "error",
                    },
                    status=401,
                ),
            )
        elif len(parts) > 2:
            raise HTTPUnauthorized(
                reason="Invalid token header. Token contains spaces",
                body=json_response(
                    {
                        "message": "Invalid token header. Token contains spaces",
                        "status": "error",
                    },
                    status=401,
                ),
            )

        token = parts[1]
        request.token = token
        return await handler(request)

    return _token_required
