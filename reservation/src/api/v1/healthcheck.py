from fastapi import APIRouter, status

router = APIRouter()


@router.get(
    "/",
    summary="Проверка состояния сервиса",
    description="Возвращает статус работы сервиса. Используется для проверки доступности API.",
    status_code=status.HTTP_200_OK
)
async def healthcheck():
    return {"status": "ok"}
