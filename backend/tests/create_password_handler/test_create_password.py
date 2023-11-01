import json
import pytest

from crypt import AES
from tests.conftest import _get_test_db


@pytest.mark.parametrize(
    "service_name, password_data, expected_status_code, expected_detail",
    [
        (
                "yandex.ru",
                {"password": "12345", },
                200,
                {
                    "service_name": "yandex.ru",
                    "password": "12345"
                }
        ),
        (
                "yandex.ru",
                {"password": "23451", },
                200,
                {
                    "service_name": "yandex.ru",
                    "password": "23451"
                }
        ),
        (
                "mail.ru",
                {"password": "qwerty", },
                200,
                {
                    "service_name": "mail.ru",
                    "password": "qwerty"
                }
        ),
    ],
)
async def test_create_password_handler(
        client, service_name, password_data, expected_status_code, expected_detail
):
    response = await client.post(f"/password/{service_name}", data=json.dumps(password_data))
    data_from_response = response.json()
    assert response.status_code == expected_status_code
    assert data_from_response == expected_detail

