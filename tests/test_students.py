from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base, get_db
from app.main import app


test_engine = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestSessionLocal = sessionmaker(
    bind=test_engine,
    autoflush=False,
    autocommit=False,
)

Base.metadata.create_all(bind=test_engine)


def override_get_db():
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


def setup_function():
    Base.metadata.drop_all(bind=test_engine)
    Base.metadata.create_all(bind=test_engine)


def test_health_check():
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_create_and_list_student():
    student = {
        "name": "Ananya Rao",
        "email": "ananya@example.com",
        "course": "TypeScript",
        "grade": 90,
        "status": "Active",
        "photoUrl": None,
    }

    create_response = client.post("/api/v1/students/", json=student)

    assert create_response.status_code == 201
    assert create_response.json()["name"] == "Ananya Rao"
    assert create_response.json()["id"] > 0

    list_response = client.get("/api/v1/students/")

    assert list_response.status_code == 200
    assert len(list_response.json()) == 1
    assert list_response.json()[0]["email"] == "ananya@example.com"


def test_reject_invalid_grade():
    student = {
        "name": "Test Student",
        "email": "test@example.com",
        "course": "Python",
        "grade": 150,
        "status": "Active",
    }

    response = client.post("/api/v1/students/", json=student)
    assert response.status_code == 422