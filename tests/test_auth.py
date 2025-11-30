import pytest
from fastapi.testclient import TestClient

from app.main import app


def test_register_and_login():
	client = TestClient(app)

	# register
	r = client.post("/auth/register", json={"username": "alice", "email": "alice@example.com", "password": "s3cr3t"})
	assert r.status_code == 200
	data = r.json()
	assert "access_token" in data

	# login via /auth/token
	r2 = client.post("/auth/token", data={"username": "alice", "password": "s3cr3t"})
	assert r2.status_code == 200
	data2 = r2.json()
	assert "access_token" in data2

