from http import HTTPStatus

import pytest_asyncio
from tests.settings import test_settings

from schemas import TableCreateTest, TableResponseTest

ENDPOINT_TABLE = test_settings.endpoint_table


@pytest_asyncio.fixture(scope='session')
async def table_create(make_request):
    async def inner():
        table_data = TableCreateTest()

        status, response = await make_request(endpoint=ENDPOINT_TABLE, method='POST', data=table_data.model_dump_json())

        if status == HTTPStatus.CREATED:
            table_res = TableResponseTest(**response)
            return status, table_res, table_data
        else:
            return status, response, table_data

    return inner
