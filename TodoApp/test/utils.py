import pytest
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool.impl import StaticPool
from fastapi.testclient import TestClient

from ..database import Base
from ..main import app
from ..models import  Todos, User
from ..routers.users import bcrypt_context


SQLALCHEMY_DATABASE_URL = "sqlite:///./testdb.db"

test_engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)

TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)

Base.metadata.create_all(bind=test_engine)


def override_get_db():
    test_db = TestSessionLocal()
    try:
        yield test_db
    finally:
        test_db.close()


def override_get_current_user():
    return {"username": "test_user", "id": 1, "user_role": "admin"}


client = TestClient(app)

@pytest.fixture
def test_todo():
    todo = Todos(title="Learn FastAPI",
                 description="Learn FastAPI from basics to advanced concepts",
                 priority=5,
                 complete=False,
                 owner_id=1)
    db = TestSessionLocal()
    db.add(todo)
    db.commit()
    yield todo

    with test_engine.connect() as connection:
        connection.execute(text("DELETE FROM todos;"))
        connection.commit()


@pytest.fixture
def test_user():
    user = User(username="test_user",
                email="test_user@test_user.com",
                first_name="Test",
                last_name="User",
                hashed_password=bcrypt_context.hash("test"),
                role="admin",
                phone_number="1234567890")
    db = TestSessionLocal()
    db.add(user)
    db.commit()
    yield user

    with test_engine.connect() as connection:
        connection.execute(text("DELETE FROM users;"))
        connection.commit()
