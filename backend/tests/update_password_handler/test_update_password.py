import json


async def test_update_password(
    client
):
    service_name1 = "google.com"
    google_password_data = {
        "password": "12345"
    }
    google_updated_password_data = {
        "password": "23456"
    }

    service_name2 = "yandex.ru"
    yandex_password_data = {
        "password": "12345"
    }

    response = await client.post(f"/password/{service_name1}", data=json.dumps(google_password_data))
    data_from_response = response.json()
    assert response.status_code == 200
    assert data_from_response == {"service_name": service_name1, "password": google_password_data["password"]}

    response = await client.post(f"/password/{service_name2}", data=json.dumps(yandex_password_data))
    data_from_response = response.json()
    assert response.status_code == 200
    assert data_from_response == {"service_name": service_name2, "password": yandex_password_data["password"]}

    response = await client.post(f"/password/{service_name1}", data=json.dumps(google_updated_password_data))
    data_from_response = response.json()
    assert response.status_code == 200
    assert data_from_response == {"service_name": service_name1, "password": google_updated_password_data["password"]}
