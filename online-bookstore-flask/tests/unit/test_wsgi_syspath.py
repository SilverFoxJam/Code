import os
import sys
import runpy


def test_wsgi_inserts_project_root_into_syspath():
    path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "wsgi.py"))
    root = os.path.dirname(path)

    original = list(sys.path)
    while root in sys.path:
        sys.path.remove(root)

    try:
        ns = runpy.run_path(path, run_name="__wsgi_test__")
        assert root in sys.path
        assert "app" in ns and ns["app"] is not None
    finally:
        sys.path[:] = original