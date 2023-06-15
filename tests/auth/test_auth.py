from fastapi.testclient import TestClient

from src.main import app

client = TestClient(app)

TEST_EMAIL = "john@doe.com"
TEST_PASSWORD = "abcdabcd"
TEST_FIRST_NAME = "John"
TEST_LAST_NAME = "Doe"
TEST_ADDRESS = "1234 Main St"
TEST_PHONE = "12341234"
TEST_ID = ""
TOKEN = ""

def test_register():
    response = client.post("/api/v1/auth/register", json={
        "email": TEST_EMAIL,
        "password": TEST_PASSWORD,
        "confirm_password": TEST_PASSWORD,
        "phone": TEST_PHONE,
        "first_name": TEST_FIRST_NAME,
        "last_name": TEST_LAST_NAME,
        "address": TEST_ADDRESS,
    })
    assert response.status_code == 200
    data = response.json()
    assert 'id' in data
    assert data['id'] != ""
    global TEST_ID
    TEST_ID = data['id']
    assert data.get("email") == TEST_EMAIL
    assert data.get("phone") == TEST_PHONE
    assert data.get("first_name") == TEST_FIRST_NAME
    assert data.get("last_name") == TEST_LAST_NAME
    assert data.get("address") == TEST_ADDRESS
    assert data.get("organization_id") == ""
    assert "password" not in data

def test_login():
    response = client.post("/api/v1/auth/login", json={
        "email": TEST_EMAIL,
        "password": TEST_PASSWORD,
    })
    assert response.status_code == 200
    data = response.json()
    assert 'token' in data
    assert data['token'] != ""
    assert data.get('user') is not None
    assert data['user'].get('id') == TEST_ID
    global TOKEN
    TOKEN = data['token']

def test_get_account():
    response = client.get("/api/v1/auth/account", headers={
        'Authorization': f"Bearer {TOKEN}"
    })
    assert response.status_code == 200
    data = response.json()
    assert 'id' in data
    assert data['id'] == TEST_ID
    assert data.get("email") == TEST_EMAIL
    assert 'password' not in data