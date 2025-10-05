from fastapi.testclient import TestClient
from main import app
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from base import Base
from database import get_db
import pytest

# Setup an in-memory SQLite database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


@pytest.fixture(scope="function")
def db_session():
    connection = engine.connect()
    transaction = connection.begin()
    db = TestingSessionLocal(bind=connection)
    yield db
    db.close()
    transaction.rollback()
    connection.close()


@pytest.fixture(scope="function")
def client(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            db_session.close()

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c


def test_create_item(client: TestClient):
    response = client.post(
        "/api/v1/items",
        json={
            "name": "Test Item",
            "description": "A test item description",
            "price": 10.0,
            "tax": 1.0,
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Test Item"
    assert data["description"] == "A test item description"
    assert data["price"] == 10.0
    assert data["tax"] == 1.0
    assert "id" in data


def test_read_items(client: TestClient):
    client.post(
        "/api/v1/items",
        json={"name": "Item 1", "price": 10.0},
    )
    client.post(
        "/api/v1/items",
        json={"name": "Item 2", "price": 20.0},
    )

    response = client.get("/api/v1/items")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["name"] == "Item 1"
    assert data[1]["name"] == "Item 2"


def test_read_single_item(client: TestClient):
    post_response = client.post(
        "/api/v1/items",
        json={"name": "Single Item", "price": 15.0},
    )
    item_id = post_response.json()["id"]

    get_response = client.get(f"/api/v1/items/{item_id}")
    assert get_response.status_code == 200
    data = get_response.json()
    assert data["name"] == "Single Item"
    assert data["id"] == item_id


def test_read_nonexistent_item(client: TestClient):
    response = client.get("/api/v1/items/nonexistent_id")
    assert response.status_code == 404
    assert response.json() == {"detail": "Item not found"}


def test_update_item(client: TestClient):
    post_response = client.post(
        "/api/v1/items",
        json={"name": "Old Name", "price": 5.0},
    )
    item_id = post_response.json()["id"]

    update_response = client.put(
        f"/api/v1/items/{item_id}",
        json={"name": "New Name", "price": 7.5},
    )
    assert update_response.status_code == 200
    data = update_response.json()
    assert data["name"] == "New Name"
    assert data["price"] == 7.5
    assert data["id"] == item_id


def test_update_nonexistent_item(client: TestClient):
    response = client.put(
        "/api/v1/items/nonexistent_id",
        json={"name": "New Name", "price": 7.5},
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "Item not found"}


def test_delete_item(client: TestClient):
    post_response = client.post(
        "/api/v1/items",
        json={"name": "Item to Delete", "price": 25.0},
    )
    item_id = post_response.json()["id"]

    delete_response = client.delete(f"/api/v1/items/{item_id}")
    assert delete_response.status_code == 204

    get_response = client.get(f"/api/v1/items/{item_id}")
    assert get_response.status_code == 404


def test_delete_nonexistent_item(client: TestClient):
    response = client.delete("/api/v1/items/nonexistent_id")
    assert response.status_code == 404
    assert response.json() == {"detail": "Item not found"}