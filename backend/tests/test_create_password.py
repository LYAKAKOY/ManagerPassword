import json

async def test_create_user(client):
    password_data = {
      "password": "12345",
    }
    resp = client.post("/password/yandex/", data=json.dumps(password_data))
    data_from_resp = resp.json()
    assert resp.status_code == 200
    assert data_from_resp["service_name"] == "yandex"
    assert data_from_resp["password"] == password_data["password"]