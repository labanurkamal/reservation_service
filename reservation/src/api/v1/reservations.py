from typing import Annotated

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, status

from dependencies.container import Container
from schemas import ReservationsResponse, ReservationsCreate
from services.reservations import ReservationService
from .dependencies import Pagination, reservation_by_id

router = APIRouter()


@router.get(
    "/",
    summary="Получить список броней",
    description="Возвращает список всех активных броней в системе.",
    status_code=status.HTTP_200_OK,
    response_model=list[ReservationsResponse],
)
@inject
async def get_reservations(
        reservation_service: Annotated[ReservationService, Depends(Provide[Container.reservation_service])],
        pg: Annotated[Pagination, Depends(Pagination)]
) -> list[ReservationsResponse]:
    return await reservation_service.get_list_reservation(offset=pg.page_num, limit=pg.page_size)


@router.post(
    "/",
    summary="Создать новую бронь",
    description="Создает новую бронь на выбранный столик и время.",
    status_code=status.HTTP_201_CREATED,
    response_model=ReservationsResponse,
)
@inject
async def create_reservation(
        reservation: ReservationsCreate,
        reservation_service: Annotated[ReservationService, Depends(Provide[Container.reservation_service])]
) -> ReservationsResponse:
    return await reservation_service.create_reservation(reservation)


@router.delete(
    "/{id}",
    summary="Удалить бронь",
    description="Удаляет бронь по указанному идентификатору.",
    status_code=status.HTTP_204_NO_CONTENT,
)
@inject
async def delete_reservation(
        reservation: Annotated[ReservationsResponse, Depends(reservation_by_id)],
        reservation_service: Annotated[ReservationService, Depends(Provide[Container.reservation_service])]
):
    return await reservation_service.delete_reservation(instance=reservation)
