from app import app

def test_health():
    client = app.test_client()
    r = client.get("/health")
    assert r.status_code == 200

def test_add_and_list():
    client = app.test_client()
    client.post("/todos", json={"title": "learn devops"})
    r = client.get("/todos")
    assert any(t["title"] == "learn devops" for t in r.get_json())