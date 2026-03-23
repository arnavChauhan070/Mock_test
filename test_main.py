import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

#  Fixture (setup reusable data)
@pytest.fixture
def sample_student():
    return {
        "name": "Test User",
        "age": 20,
        "course": "CSE"
    }

#  Test API: POST /students
def test_create_student(sample_student):
    response = client.post("/students", json=sample_student)
    
    assert response.status_code == 201
    data = response.json()
    
    assert data["name"] == "Test User"
    assert data["age"] == 20
    assert data["course"] == "CSE"

#  Test API: GET /students
def test_get_students():
    response = client.get("/students")
    
    assert response.status_code == 200
    assert isinstance(response.json(), list)

#  Test FUNCTION (simple example)
def add(a, b):
    return a + b

def test_add_function():
    result = add(2, 3)
    assert result == 5