from wsgi import app


def test_app_imports_and_basic_get():
    assert app is not None
    client = app.test_client()
    resp = client.get("/")
    assert resp.status_code in (200, 302, 404)