from http import HTTPStatus

import pytest

from tests.settings import test_settings

ENDPOINT_RESERVATION = test_settings.endpoint_reservation
ENDPOINT_TABLE = test_settings.endpoint_table


@pytest.mark.asyncio
class TestReservation:

    async def test_create_reservation(self, table_create, reservation_create):
        status, table_response, table_expected_data = await table_create()

        assert status == HTTPStatus.CREATED
        assert table_response.model_dump() == {
            'id': 1,
            'name': table_expected_data.name,
            'seats': table_response.seats,
            'location': table_response.location
        }

        status, recerv_response, recerv_expected_data = await reservation_create(table_id=table_response.id, mins=30)

        assert status == HTTPStatus.CREATED
        assert recerv_response.model_dump(exclude={"reservation_time"}) == {
            'id': 1,
            'customer_name': recerv_expected_data.customer_name,
            'duration_minutes': recerv_expected_data.duration_minutes,
            'table': table_response.model_dump()
        }

        status, recerv_response, recerv_expected_data = await reservation_create(table_id=table_response.id, mins=30)

        assert status == HTTPStatus.CONFLICT
        assert recerv_response['detail'] == f'Столик с id {table_response.id} уже забронирован на указанное время.'

    async def test_get_reservation(self, make_request):
        status, response = await make_request(endpoint=ENDPOINT_RESERVATION)

        assert status == HTTPStatus.OK
        assert len(response) == 1

    async def test_delete_reservation(self, make_request):
        status, _ = await make_request(endpoint=ENDPOINT_RESERVATION)

        status, response = await make_request(endpoint=ENDPOINT_RESERVATION + "/1/", method='DELETE')
        assert status == HTTPStatus.NO_CONTENT
