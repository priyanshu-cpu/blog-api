import os
import pytest
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.engine import make_url
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient


TEST_DATABASE_URL = os.environ['TEST_DATABASE_URL']

db_name = make_url(TEST_DATABASE_URL).database

os.environ['SECRET_KEY'] = 'test-secret-key-for-testing-only'

test_engine = create_engine(db_name)

from database import Base, get_db
from main import app
import models

TestingSessionLocal = sessionmaker(
    bind=test_engine,
    autocommit=False,
    autoflush=False
)


@pytest.fixture(scope="function")
def setup_database():
    Base.metadata.create_all(bind=test_engine)

    yield

    Base.metadata.drop_all(bind=test_engine)


@pytest.fixture
def db_session(setup_database):

    db = TestingSessionLocal()

    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def client(setup_database):

    def override_getdb():
        db = TestingSessionLocal()

        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides(get_db) = override_getdb

