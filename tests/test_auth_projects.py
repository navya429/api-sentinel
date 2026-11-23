def register_and_login(client, email="qa@example.com"):
    created = client.post("/api/v1/users/register", json={"email": email, "password": "StrongPassword123!"})
    assert created.status_code == 201
    token = client.post("/api/v1/auth/login", data={"username": email, "password": "StrongPassword123!"})
    assert token.status_code == 200
    return {"Authorization": f"Bearer {token.json()['access_token']}"}

def test_registration_duplicate_and_login(client):
    payload = {"email": "qa@example.com", "password": "StrongPassword123!"}
    assert client.post("/api/v1/users/register", json=payload).status_code == 201
    assert client.post("/api/v1/users/register", json=payload).status_code == 409
    assert client.post("/api/v1/auth/login", data={"username": payload["email"], "password": payload["password"]}).status_code == 200

def test_project_crud_requires_auth_and_persists(client):
    assert client.get("/api/v1/projects").status_code == 401
    headers = register_and_login(client)
    created = client.post("/api/v1/projects", headers=headers, json={
        "name": "QA project", "description": "test project", "base_url": "https://example.com"
    })
    assert created.status_code == 201, created.text
    project_id = created.json()["id"]
    assert client.get("/api/v1/projects", headers=headers).json()[0]["id"] == project_id
    updated = client.put(f"/api/v1/projects/{project_id}", headers=headers, json={"name": "Updated QA"})
    assert updated.status_code == 200
    assert updated.json()["name"] == "Updated QA"
    assert client.delete(f"/api/v1/projects/{project_id}", headers=headers).status_code == 204
    assert client.get(f"/api/v1/projects/{project_id}", headers=headers).status_code == 404

def test_users_cannot_access_other_users_projects(client):
    owner_headers = register_and_login(client, "owner@example.com")
    other_headers = register_and_login(client, "other@example.com")
    created = client.post("/api/v1/projects", headers=owner_headers, json={"name": "Private", "base_url": "https://example.com"})
    project_id = created.json()["id"]
    assert client.get(f"/api/v1/projects/{project_id}", headers=other_headers).status_code == 404
