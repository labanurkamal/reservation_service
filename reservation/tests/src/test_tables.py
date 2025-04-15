from http import HTTPStatus

import pytest

from tests.settings import test_settings

ENDPOINT_RESERVATION = test_settings.endpoint_reservation
ENDPOINT_TABLE = test_settings.endpoint_table


@pytest.mark.asyncio
class TestTable:

    async def test_create_table(self, table_create):
        status, table_response, table_expected_data = await table_create()

        assert status == HTTPStatus.CREATED
        assert table_response.model_dump() == {
            'id': 1,
            'name': table_expected_data.name,
            'seats': table_response.seats,
            'location': table_response.location
        }

        status, table_response, _ = await table_create()

        assert status == HTTPStatus.CONFLICT
        assert table_response['detail'] == "Table с такими данными уже существует."

    async def test_get_tables(self, make_request):
        status, response = await make_request(endpoint=ENDPOINT_TABLE)

        assert status == HTTPStatus.OK
        assert len(response) == 1

    async def test_delete_table(self, make_request):
        status, response = await make_request(endpoint=ENDPOINT_TABLE + "/1/", method='DELETE')
        assert status == HTTPStatus.NO_CONTENT
