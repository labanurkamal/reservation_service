from pathlib import Path
from typing import Annotated

from dependency_injector.wiring import Provide, inject
from fastapi import Query, Depends

from dependencies.container import Container
from schemas import TableResponse, ReservationsResponse
from services.reservations import ReservationService
from services.tables import TableService

PAGE_SIZE_MIN: int = 1
PAGE_SIZE_MAX: int = 50
PAGE_NUM: int = 1

PageSize = Annotated[int, Query(ge=PAGE_SIZE_MIN, le=PAGE_SIZE_MAX, description="Кол-во результатов на странице.")]
PageNum = Annotated[int, Query(ge=PAGE_NUM, le=PAGE_SIZE_MAX, description="Номер страницы.")]


class Pagination:
    def __init__(
            self,
            page_size: PageSize = PAGE_SIZE_MAX,
            page_num: PageNum = PAGE_NUM,
    ) -> None:
        self.page_size = page_size
        self.page_num = (page_num - 1) * self.page_size


@inject
async def table_by_id(
        id: Annotated[int, Path],
        table_service: Annotated[TableService, Depends(Provide[Container.table_service])]
) -> TableResponse:
    return await table_service.get_table(id)


@inject
async def reservation_by_id(
        id: Annotated[int, Path],
        reservation_service: Annotated[ReservationService, Depends(Provide[Container.reservation_service])]
) -> ReservationsResponse:
    return await reservation_service.get_reservation(reservation_id=id)
