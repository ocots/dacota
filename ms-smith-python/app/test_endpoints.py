from app.main import app, get_settings
from fastapi.testclient import TestClient

client = TestClient(app)


def test_get_home():
    response = client.get("/")
    assert response.status_code == 200
    assert response.headers["content-type"] == "text/html; charset=utf-8"


def test_post_home():
    response = client.post("/")
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/json"
    assert response.json() == {"Hello": "World"}


def test_post_parameters_echo():
    data = {
        "c1": [7.11714, 1210.595, 229.664],
        "c2": [6.95465, 1170.966, 226.232],
        "c3": [8.08097, 1582.271, 239.726],
        "a": [
            [0, -643.277, 184.701],
            [228.457, 0, 2736.86],
            [222.645, -1244.03, 0],
        ],
        "alpha": [[0, 0.3043, 0.3084], [0.3043, 0, 0.095], [0.3084, 0.095, 0]],
    }
    response = client.post("/parameters-echo/", json=data)
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/json"
    assert response.json() == data


def test_post_ternary_diagram_with_missing_parameters():
    settings = get_settings()
    data = {
        "c1": [7.11714, 1210.595, 229.664],
        "c2": [6.95465, 1170.966, 226.232],
        "c3": [8.08097, 1582.271, 239.726],
        "a": [
            [0, -643.277, 184.701],
            [228.457, 0, 2736.86],
            [222.645, -1244.03, 0],
        ],
    }
    response = client.post(
        "/ternary-diagram/",
        json=data,
        headers={"Authorization": f"Ayman {settings.app_auth_token}"},
    )
    assert response.status_code == 400
    assert response.headers["content-type"] == "application/json"
    assert response.json() == {"detail": "Missing one or more parameters"}


def test_post_ternary_diagram_with_invalid_parameters():
    settings = get_settings()

    data = {
        "c1": [7.11714, 1210.595],
        "c2": [6.95465, 1170.966, 226.232],
        "c3": [8.08097, 1582.271, 239.726],
        "a": [
            [0, -643.277, 184.701],
            [228.457, 0, 2736.86],
            [222.645, -1244.03, 0],
        ],
        "alpha": [[0, 0.3043, 0.3084], [0.3043, 0, 0.095], [0.3084, 0.095, 0]],
    }
    response = client.post(
        "/ternary-diagram/",
        json=data,
        headers={"Authorization": f"Ayman {settings.app_auth_token}"},
    )
    assert response.status_code == 400
    assert response.headers["content-type"] == "application/json"
    assert response.json() == {"detail": "Invalid parameters"}


def test_post_ternary_diagram_with_invalid_parameters2():
    settings = get_settings()

    data = {
        "c1": [7.11714, 1210.595, 0],
        "c2": [6.95465, -1170.966, 226.232],
        "c3": [8.08097, 1582.271, 239.726],
        "a": [
            [0, -643.277, 184.701],
            [228.457, 0, "2736.86"],
            [222.645, -1244.03, 0],
        ],
        "alpha": [[0, 0.3043, 0.3084], [0.3043, 0, 0.095], [0.3084, 0.095, 0]],
    }
    response = client.post(
        "/ternary-diagram/",
        json=data,
        headers={"Authorization": f"Ayman {settings.app_auth_token}"},
    )
    assert response.status_code == 400
    assert response.headers["content-type"] == "application/json"
    assert response.json() == {"detail": "Invalid parameters"}


def test_post_ternary_diagram_with_no_token():
    data = {
        "c1": [7.11714, 1210.595, 229.664],
        "c2": [6.95465, 1170.966, 226.232],
        "c3": [8.08097, 1582.271, 239.726],
        "a": [
            [0, -643.277, 184.701],
            [228.457, 0, 2736.86],
            [222.645, -1244.03, 0],
        ],
        "alpha": [[0, 0.3043, 0.3084], [0.3043, 0, 0.095], [0.3084, 0.095, 0]],
    }

    response = client.post("/ternary-diagram/", json=data)
    assert response.status_code == 401
    assert response.headers["content-type"] == "application/json"


def test_post_ternary_diagram():
    settings = get_settings()

    data = {
        "c1": [7.11714, 1210.595, 229.664],
        "c2": [6.95465, 1170.966, 226.232],
        "c3": [8.08097, 1582.271, 239.726],
        "a": [
            [0, -643.277, 184.701],
            [228.457, 0, 2736.86],
            [222.645, -1244.03, 0],
        ],
        "alpha": [[0, 0.3043, 0.3084], [0.3043, 0, 0.095], [0.3084, 0.095, 0]],
    }

    response = client.post(
        "/ternary-diagram/",
        json=data,
        headers={"Authorization": f"Ayman {settings.app_auth_token}"},
    )
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/json"
