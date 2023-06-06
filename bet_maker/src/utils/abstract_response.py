from functools import wraps
from typing import Any

from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pydantic import BaseModel


class CustomResponse(BaseModel):
    error: bool | None = False
    data: Any


def get_response(data: Any, error: bool = False, status_code: int = 200):
    data = jsonable_encoder(CustomResponse(data=data, error=error).dict())
    return JSONResponse(data, status_code=status_code)


def response_decorator(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            response = await func(*args, **kwargs)
            return get_response(response)
        except Exception as e:
            return get_response(str(e), error=True, status_code=500)
    return wrapper
