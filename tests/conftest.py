import os
os.environ["DATABASE_URL"] = "sqlite:///./test_api_sentinel.db"
os.environ["JWT_SECRET_KEY"] = "test-secret-key-only-32-bytes-minimum"
from fastapi.testclient import TestClient
import pytest
from app.db.base import Base
from app.db.session import engine
from app.main import app

@pytest.fixture()
def client():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    with TestClient(app) as test_client:
        yield test_client
    Base.metadata.drop_all(bind=engine)
