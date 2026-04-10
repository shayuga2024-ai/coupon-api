import pytest
from app import create_app

@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_list_coupons(client):
    res = client.get("/coupons")
    assert res.status_code == 200

def test_get_valid_coupon(client):
    res = client.get("/coupons/SAVE10")
    assert res.status_code == 200

def test_get_expired_coupon(client):
    res = client.get("/coupons/EXPIRED")
    assert res.status_code == 400

def test_get_nonexistent_coupon(client):
    res = client.get("/coupons/FAKE99")
    assert res.status_code == 404

def test_create_coupon(client):
    res = client.post("/coupons", json={"code": "NEW20", "discount": 20})
    assert res.status_code == 201

def test_apply_coupon(client):
    res = client.post("/apply", json={"code": "SAVE10", "price": 100})
    assert res.status_code == 200
    assert res.get_json()["final_price"] == 90.0

def test_apply_missing_fields(client):
    res = client.post("/apply", json={"code": "SAVE10"})
    assert res.status_code == 400