from pathlib import Path

from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine

from app.db import get_session
from app.main import app


def create_test_client():
    engine = create_engine("sqlite://", connect_args={"check_same_thread": False})
    SQLModel.metadata.create_all(engine)

    def override_get_session():
        with Session(engine) as session:
            yield session

    app.dependency_overrides[get_session] = override_get_session
    return TestClient(app)


def test_dashboard_loads():
    client = create_test_client()
    response = client.get("/")
    assert response.status_code == 200
    assert "Outstanding Claims" in response.text


def test_create_records_flow():
    client = create_test_client()

    child = client.post("/children", data={"full_name": "Sam Child", "date_of_birth": "2018-05-01"})
    therapist = client.post(
        "/therapists",
        data={"full_name": "Dr. Jay", "specialty": "Speech", "provider_number": "PN-01"},
    )
    assert child.status_code == 303
    assert therapist.status_code == 303

    children_page = client.get("/children")
    therapists_page = client.get("/therapists")
    assert "Sam Child" in children_page.text
    assert "Dr. Jay" in therapists_page.text
