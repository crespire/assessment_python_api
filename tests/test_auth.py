import json


def test_login(client):
    """should allow login request from thomas."""
    response = client.post(
        "/api/login",
        data=json.dumps(dict(username="thomas", password="123456")),
        content_type="application/json",
    )
    values = response.json
    assert values.get("username") == "thomas"
    assert values.get("id") == 1
    assert response.status_code == 200
