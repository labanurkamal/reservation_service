from typing import Annotated

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, status, Depends

from dependencies.container import Container
from schemas import TableCreate, TableResponse, TableOutWithReservations
from services.tables import TableService
# from schemas.tables import TableOutWithReservations
from .dependencies import Pagination
from .dependencies import table_by_id

router = APIRouter()


@router.get(
    "/reservations",
    summary="Список столиков с бронями",
    description="Получает список всех столиков в ресторане вместе с информацией о текущих бронированиях. "
                "Полезно для отображения занятости столиков и управления бронями.",
    status_code=status.HTTP_200_OK,
    response_model=list[TableOutWithReservations],
)
@inject
async def get_tables_with_reservations(
        table_service: Annotated[TableService, Depends(Provide[Container.table_service])],
) -> list[TableOutWithReservations]:
    return await table_service.get_table_with_reservations()


@router.get(
    "/",
    summary="Получить список столиков",
    description="Возвращает список всех доступных столиков в ресторане.",
    status_code=status.HTTP_200_OK,
    response_model=list[TableResponse],
)
@inject
async def get_tables(
        table_service: Annotated[TableService, Depends(Provide[Container.table_service])],
        pg: Annotated[Pagination, Depends(Pagination)]
) -> list[TableResponse]:
    return await table_service.get_list_tables(offset=pg.page_num, limit=pg.page_size)


@router.post(
    "/",
    summary="Создать новый столик",
    description="Создает новый столик с заданными параметрами: название, количество мест и расположение.",
    status_code=status.HTTP_201_CREATED,
    response_model=TableResponse,
)
@inject
async def create_table(
        table: TableCreate,
        table_service: Annotated[TableService, Depends(Provide[Container.table_service])],
) -> TableResponse:
    return await table_service.create_table(instance=table)


@router.delete(
    "/{id}",
    summary="Удалить столик",
    description="Удаляет столик по его идентификатору, если он не используется в активных бронях.",
    status_code=status.HTTP_204_NO_CONTENT,
)
@inject
async def delete_table(
        table_service: Annotated[TableService, Depends(Provide[Container.table_service])],
        table: TableResponse = Depends(table_by_id),
):
    return await table_service.delete_table(instance=table)
