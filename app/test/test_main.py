from fastapi.testclient import TestClient
from fastapi import FastAPI
from datetime import datetime
import sys
from pathlib import Path
sys.path[0] = str(Path(sys.path[0]).parent)
from app import main
# app = FastAPI()
client = TestClient(main.app)


def test_default():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message":"hello world"}


def test_get_notes():
    response = client.get("/notes")
    assert response.status_code == 401

def test_create_user():
    response = client.post("/users/", json={"email":"vincentchrisbone@gmail.com","password":123456})
    assert response.status_code == 201
    assert response.json() == {
        "id":1,
        "email":"vincentchrisbone@gmail.com",
        "created_at":datetime.utcnow(),
    }
