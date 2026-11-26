"""Verificación del contrato HTTP y paridad del simulador."""
import pytest
from fastapi.testclient import TestClient

from api import app
from src.predictor import Profile, predict_profile

EXAMPLE = {"age": 30, "sex": "male", "bmi": 25.0, "children": 0,
           "smoker": "no", "region": "northeast"}


@pytest.fixture
def client():
    with TestClient(app) as test_client:
        yield test_client


def test_health_and_swagger(client):
    assert client.get("/health").json() == {"status": "ok"}
    assert client.get("/docs").status_code == 200
    assert "/predict" in client.get("/openapi.json").json()["paths"]


def test_prediction_matches_local_inference(client):
    response = client.post("/predict", json=EXAMPLE)
    assert response.status_code == 200
    expected = predict_profile(app.state.model, Profile(**EXAMPLE))
    assert response.json() == {"predicted_charges": expected}
    assert expected > 0


@pytest.mark.parametrize("changes", [
    {"age": 17}, {"age": "30"}, {"bmi": 53.14}, {"children": 6},
    {"smoker": "sometimes"}, {"region": "north"}, {"extra": 1},
])
def test_invalid_profiles(client, changes):
    assert client.post("/predict", json=EXAMPLE | changes).status_code == 422


def test_missing_field(client):
    payload = {key: value for key, value in EXAMPLE.items() if key != "bmi"}
    assert client.post("/predict", json=payload).status_code == 422
