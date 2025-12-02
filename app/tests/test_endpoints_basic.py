import os
from fastapi.testclient import TestClient

def test_regions_endpoints():
    os.environ["DATABASE_URL"] = "sqlite+pysqlite:///:memory:"
    from app.main import create_app
    app = create_app()
    client = TestClient(app)
    # create
    r = client.post("/api/v1/regions/", json={"name": "测试区域", "location": None})
    assert r.status_code == 200
    data = r.json()
    assert data["name"] == "测试区域"
    rid = data["id"]
    # list
    r2 = client.get("/api/v1/regions/")
    assert r2.status_code == 200
    lst = r2.json()
    assert any(x["id"] == rid for x in lst)
