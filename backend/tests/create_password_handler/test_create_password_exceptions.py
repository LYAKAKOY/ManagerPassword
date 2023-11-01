import json

import pytest


@pytest.mark.parametrize(
    "service_name, password_data, expected_status_code, expected_detail",
    [
        (
                "google.com",
                {},
                422,
                {'detail': [
                    {'input': {},
                     'loc': ['body', 'password'],
                     'msg': 'Field required',
                     'type': 'missing',
                     'url': 'https://errors.pydantic.dev/2.4/v/missing'
                     }
                ]
                }
        ),
    ],
)
async def test_create_password_exceptions(
        client, service_name, password_data, expected_status_code, expected_detail
):
    response = await client.post(f"/password/{service_name}", data=json.dumps(password_data))
    data_from_response = response.json()
    assert response.status_code == expected_status_code
    assert data_from_response == expected_detail
