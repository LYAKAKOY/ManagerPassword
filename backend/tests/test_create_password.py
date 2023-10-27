import json

import pytest


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
        # (
        #         "yandex.ru",
        #         {"password": "23451", },
        #         200,
        #         {
        #             "service_name": "yandex.ru",
        #             "password": "23451"
        #         }
        # ),
        (
                "mail.ru",
                {"password": "qwerty", },
                200,
                {
                    "service_name": "yandex.ru",
                    "password": "qwerty"
                }
        ),
    ],
)
async def test_create_password(
    client, service_name, password_data, expected_status_code, expected_detail
):
    resp = client.post(f"/password/{service_name}/", data=json.dumps(password_data))
    data_from_resp = resp.json()
    assert resp.status_code == expected_status_code
    assert data_from_resp == expected_detail

# async def test_create_password(client):
#     password_data = {
#       "password": "12345",
#     }
#     resp = client.post("/password/yandex/", data=json.dumps(password_data))
#     data_from_resp = resp.json()
#     assert resp.status_code == 200
#     assert data_from_resp["service_name"] == "yandex"
#     assert data_from_resp["password"] == password_data["password"]