import os
from dotenv import load_dotenv
import pytest
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.engine import make_url
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

load_dotenv()

TEST_DATABASE_URL = os.environ['TEST_DATABASE_URL']

# db_name = make_url(TEST_DATABASE_URL).database

os.environ['SECRET_KEY'] = 'test-secret-key-for-testing-only'

test_engine = create_engine(TEST_DATABASE_URL)

from database import Base, get_db
from main import app
import models



@pytest.fixture(scope="session", autouse=True)
def setup_database():
    Base.metadata.create_all(bind=test_engine)
    yield
    Base.metadata.drop_all(bind=test_engine)


@pytest.fixture(scope="function")
def db_session(setup_database):
    conn = test_engine.connect()
    transaction = conn.begin()


    TestingSessionLocal = sessionmaker(
        bind=conn,
        autoflush=False,
        autocommit= False,
        join_transaction_mode= "create_savepoint"
    )

    session = TestingSessionLocal()

    try:
        yield session
    finally:
        session.close()
        transaction.rollback()
        conn.close()



@pytest.fixture(scope="function")
def client(db_session):

    def override_getdb():
        yield db_session

    app.dependency_overrides[get_db] = override_getdb

    try:
        with TestClient(app) as test_client:
            yield test_client

    finally:
        app.dependency_overrides.pop(get_db, None)

        
@pytest.fixture
def user_data():
    return {
        "username": "testuser",
        "email": "test@example.com",
        "password": "test@1"
    }


@pytest.fixture
def registered_user(client, user_data):

    response = client.post(
        "/register",
        json=user_data
    )

    assert response.status_code == 201

    return user_data


@pytest.fixture
def auth_headers(client, registered_user):

    response = client.post(
        "/login",
        data={
            "username": registered_user["username"],
            "password": registered_user["password"]
        }
    )

    assert response.status_code == 200

    token = response.json()["access_token"]

    return {
        "Authorization": f"Bearer {token}"
    }


@pytest.fixture
def post_data():
    return {
        "title": "My First Blog",
        "content": "Learning pytest with FastAPI"
    }


@pytest.fixture
def created_post(client, auth_headers, post_data):

    response = client.post(
        "/blogs",
        json=post_data,
        headers=auth_headers
    )

    assert response.status_code == 201

    return response.json()

