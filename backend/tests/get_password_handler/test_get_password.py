import json

import pytest


@pytest.mark.parametrize(
    "service_name, expected_status_code, password_data, expected_detail",
    [
        (
            "yandex.ru",
            200,
            {"password": "23451"},
            {"service_name": "yandex.ru", "password": "23451"},
        ),
        (
            "mail.ru",
            200,
            {"password": "qwerty"},
            {"service_name": "mail.ru", "password": "qwerty"},
        ),
    ],
)
async def test_get_password(
    client,
    create_test_auth_headers_for_user,
    service_name,
    expected_status_code,
    password_data,
    expected_detail,
):
    await client.post(
        f"/password/{service_name}",
        data=json.dumps(password_data),
        headers=create_test_auth_headers_for_user,
    )
    response = await client.get(
        f"/password/{service_name}", headers=create_test_auth_headers_for_user
    )
    data_from_response = response.json()
    assert response.status_code == expected_status_code
    assert data_from_response == expected_detail


@pytest.mark.parametrize(
    "service_name_part, expected_status_code, expected_detail",
    [
        (
            ".ru",
            200,
            [
                {"service_name": "yandex.ru", "password": "23451"},
                {"service_name": "mail.ru", "password": "qwerty"},
            ],
        ),
    ],
)
async def test_get_passwords_by_match(
    client,
    create_test_auth_headers_for_user,
    service_name_part,
    expected_status_code,
    expected_detail,
):
    for service in expected_detail:
        await client.post(
            f"/password/{service['service_name']}",
            data=json.dumps({"password": service["password"]}),
            headers=create_test_auth_headers_for_user,
        )
    response = await client.get(
        f"/password/?service_name={service_name_part}",
        headers=create_test_auth_headers_for_user,
    )
    data_from_response = response.json()
    assert response.status_code == expected_status_code
    assert data_from_response == expected_detail
