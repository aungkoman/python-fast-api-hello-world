import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from base import Base
from models import Item, ItemCreate, ItemUpdate
from services import item_service

# Setup an in-memory SQLite database for testing
@pytest.fixture(scope="function")
def db_session():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

def test_create_item(db_session: Session):
    item_data = ItemCreate(name="Test Item", description="A test item", price=10.0, tax=1.0)
    item = item_service.create_item(db_session, item_data)
    assert item.name == "Test Item"
    assert item.description == "A test item"
    assert item.price == 10.0
    assert item.tax == 1.0
    assert item.id is not None

def test_get_items(db_session: Session):
    item_data1 = ItemCreate(name="Item 1", price=10.0)
    item_service.create_item(db_session, item_data1)
    item_data2 = ItemCreate(name="Item 2", price=20.0)
    item_service.create_item(db_session, item_data2)

    items = item_service.get_items(db_session)
    assert len(items) == 2
    assert items[0].name == "Item 1"
    assert items[1].name == "Item 2"

def test_get_item(db_session: Session):
    item_data = ItemCreate(name="Single Item", price=15.0)
    created_item = item_service.create_item(db_session, item_data)

    fetched_item = item_service.get_item(db_session, created_item.id)
    assert fetched_item.name == "Single Item"
    assert fetched_item.id == created_item.id

def test_update_item(db_session: Session):
    item_data = ItemCreate(name="Old Name", price=5.0)
    created_item = item_service.create_item(db_session, item_data)

    update_data = ItemUpdate(name="New Name", price=7.5)
    updated_item = item_service.update_item(db_session, created_item.id, update_data)

    assert updated_item.name == "New Name"
    assert updated_item.price == 7.5
    assert updated_item.id == created_item.id

def test_delete_item(db_session: Session):
    item_data = ItemCreate(name="Item to Delete", price=25.0)
    created_item = item_service.create_item(db_session, item_data)

    deleted_item = item_service.delete_item(db_session, created_item.id)
    assert deleted_item.id == created_item.id

    fetched_item = item_service.get_item(db_session, created_item.id)
    assert fetched_item is None