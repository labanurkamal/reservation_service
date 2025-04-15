from http import HTTPStatus

import pytest

from tests.settings import test_settings


@pytest.mark.asyncio
async def test_app_healthcheck(make_request):
    status, response = await make_request(endpoint=test_settings.endpoint_healthcheck)

    assert status == HTTPStatus.OK
    assert response == {"status": "ok"}
