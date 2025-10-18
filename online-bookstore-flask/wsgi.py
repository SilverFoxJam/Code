# wsgi.py — robust shim so "flask --app wsgi:app ..." always works
try:
    # Try the application factory pattern first
    from app import create_app as _factory
    app = _factory(testing=False)
except Exception:
    # Fallback: import a Flask instance named "app" from app.py
    from app import app  # noqa: F401
