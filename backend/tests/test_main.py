from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_add_path_returns_json_result() -> None:
    response = client.get("/add", params={"a": 2, "b": 3})

    assert response.status_code == 200
    assert response.json() == {"result": 5.0}


def test_subtract_path_returns_json_result() -> None:
    response = client.get("/subtract", params={"a": 7, "b": 4})

    assert response.status_code == 200
    assert response.json() == {"result": 3.0}


def test_multiply_path_returns_json_result() -> None:
    response = client.get("/multiply", params={"a": 6, "b": 5})

    assert response.status_code == 200
    assert response.json() == {"result": 30.0}


def test_divide_path_returns_json_result() -> None:
    response = client.get("/divide", params={"a": 9, "b": 3})

    assert response.status_code == 200
    assert response.json() == {"result": 3.0}


def test_divide_path_returns_client_error_for_zero_divisor() -> None:
    response = client.get("/divide", params={"a": 1, "b": 0})

    assert response.status_code == 400
    assert response.json() == {"detail": "Cannot divide by zero."}
