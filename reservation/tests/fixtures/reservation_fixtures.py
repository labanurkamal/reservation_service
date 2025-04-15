from datetime import datetime, timedelta
from http import HTTPStatus

import pytest_asyncio
from tests.settings import test_settings

from schemas import ReservationCreateTest, ReservationsResponseTest

ENDPOINT_RESERVATION = test_settings.endpoint_reservation


@pytest_asyncio.fixture(scope='session')
async def reservation_create(make_request):
    async def inner(table_id: int, mins: int):
        reservation_time = (datetime.now() + timedelta(minutes=mins)).isoformat()
        reservation_data = ReservationCreateTest(reservation_time=reservation_time, table_id=table_id)

        status, response = await make_request(endpoint=ENDPOINT_RESERVATION, method='POST',
                                              data=reservation_data.model_dump_json())

        if status == HTTPStatus.CREATED:
            reservation_res = ReservationsResponseTest(**response)
            return status, reservation_res, reservation_data
        else:
            return status, response, reservation_data

    return inner
