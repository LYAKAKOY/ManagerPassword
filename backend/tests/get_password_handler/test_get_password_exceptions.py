import json
import pytest


@pytest.mark.parametrize(
    "service_name, expected_status_code, expected_detail",
    [
        (
                "google.com",
                404,
                {
                    "detail": "The password of this service not found"
                }
        ),
    ],
)
async def test_get_password_exceptions(
        client, service_name, expected_status_code, expected_detail
):
    response = await client.get(f"/password/{service_name}")
    data_from_response = response.json()
    assert response.status_code == expected_status_code
    assert data_from_response == expected_detail


@pytest.mark.parametrize(
    "service_name_part, expected_status_code, expected_detail",
    [
        (
                ".com",
                404,
                {
                    "detail": "No service found"
                }
        ),
    ],
)
async def test_get_passwords_by_match_exceptions(
        client, service_name_part, expected_status_code, expected_detail
):
    response = await client.get(f"/password/?service_name={service_name_part}")
    data_from_response = response.json()
    assert response.status_code == expected_status_code
    assert data_from_response == expected_detail
