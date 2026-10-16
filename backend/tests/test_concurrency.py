"""Exercise actual PostgreSQL locks with independent request transactions."""

from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta, timezone
from threading import Barrier

import pytest
from sqlalchemy.orm import sessionmaker
from app.database import get_db
from app.main import app

pytestmark = pytest.mark.postgres


@pytest.fixture()
def concurrent_client(client, db):
    if db.bind.dialect.name != "postgresql":
        pytest.skip("PostgreSQL is required to verify SELECT FOR UPDATE")
    factory = sessionmaker(bind=db.bind)

    def independent_session():
        with factory() as session:
            yield session

    app.dependency_overrides[get_db] = independent_session
    return client


def test_simultaneous_borrowers_cannot_overbook(concurrent_client):
    client = concurrent_client
    item = client.post(
        "/api/equipment",
        json={
            "name": "Last two cameras",
            "category": "Electronics",
            "quantity": 2,
            "location": "Test lab",
        },
    ).json()
    barrier = Barrier(6)

    def borrow(index):
        barrier.wait(timeout=10)
        return client.post(
            "/api/loans",
            json={
                "equipment_id": item["id"],
                "borrower": f"Borrower {index}",
                "due_at": (datetime.now(timezone.utc) + timedelta(days=1)).isoformat(),
            },
        ).status_code

    with ThreadPoolExecutor(max_workers=6) as pool:
        statuses = list(pool.map(borrow, range(6)))
    assert sorted(statuses) == [201, 201, 409, 409, 409, 409]
    assert len(client.get("/api/loans").json()) == 2
    assert client.get("/api/stats").json()["available"] == 0


def test_simultaneous_returns_are_applied_once(concurrent_client):
    client = concurrent_client
    item = client.post(
        "/api/equipment",
        json={
            "name": "Loaned camera",
            "category": "Electronics",
            "quantity": 1,
            "location": "Test lab",
        },
    ).json()
    loan = client.post(
        "/api/loans",
        json={
            "equipment_id": item["id"],
            "borrower": "Praneeth",
            "due_at": (datetime.now(timezone.utc) + timedelta(days=1)).isoformat(),
        },
    ).json()
    barrier = Barrier(2)

    def return_loan(_):
        barrier.wait(timeout=10)
        return client.put(f"/api/loans/{loan['id']}/return").status_code

    with ThreadPoolExecutor(max_workers=2) as pool:
        statuses = list(pool.map(return_loan, range(2)))
    assert sorted(statuses) == [200, 409]
    assert client.get("/api/stats").json()["available"] == 1
