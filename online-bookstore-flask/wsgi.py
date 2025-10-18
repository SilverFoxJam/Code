# wsgi.py — simple + robust loader for Flask app
import os
import sys

# Ensure project root is importable
ROOT = os.path.dirname(__file__)
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

# Prefer an app factory if present; fall back to a module-level "app"
try:
    from app import create_app as _factory  # type: ignore
    app = _factory(testing=False)
except Exception:
    from app import app  # noqa: F401
