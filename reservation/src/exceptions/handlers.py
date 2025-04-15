from fastapi import Request
from fastapi.responses import JSONResponse

from exceptions.base import AppException


async def app_exception_handler(request: Request, exc: AppException) -> JSONResponse:
    """
    Обработчик пользовательских исключений AppException.

    Возвращает JSON-ответ с соответствующим HTTP статусом и сообщением об ошибке.
    """

    return JSONResponse(
        status_code=exc.code,
        content={'detail': exc.detail}
    )
