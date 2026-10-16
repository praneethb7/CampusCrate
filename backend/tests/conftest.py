import os
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from sqlalchemy.engine import make_url
from app.database import Base, get_db
from app.main import app


@pytest.fixture()
def db():
    url = os.environ.get("TEST_DATABASE_URL", "sqlite://")
    parsed = make_url(url)
    if parsed.get_backend_name() != "sqlite" and not (parsed.database or "").endswith(
        "_test"
    ):
        raise ValueError(
            "TEST_DATABASE_URL must name a disposable database ending in _test"
        )
    engine = create_engine(
        url,
        **(
            {"connect_args": {"check_same_thread": False}, "poolclass": StaticPool}
            if url == "sqlite://"
            else {}
        ),
    )
    Base.metadata.create_all(engine)
    with sessionmaker(bind=engine)() as session:
        yield session
    Base.metadata.drop_all(engine)
    engine.dispose()


@pytest.fixture()
def client(db):
    def override():
        yield db

    app.dependency_overrides[get_db] = override
    with TestClient(app) as client:
        yield client
    app.dependency_overrides.clear()
