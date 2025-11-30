from fastapi.testclient import TestClient

from app.main import app


def test_create_list_message():
	client = TestClient(app)

	# create user and get token
	r = client.post("/auth/register", json={"username": "bob", "password": "pw123", "email": "bob@example.com"})
	assert r.status_code == 200
	token = r.json()["access_token"]

	headers = {"Authorization": f"Bearer {token}"}
	payload = {"title": "hello", "body": "this is a test"}
	r2 = client.post("/messages/", json=payload, headers=headers)
	assert r2.status_code == 200
	msg = r2.json()
	assert msg["title"] == "hello"

	# list messages
	r3 = client.get("/messages/")
	assert r3.status_code == 200
	data = r3.json()
	assert isinstance(data, list)
	assert any(m["title"] == "hello" for m in data)

