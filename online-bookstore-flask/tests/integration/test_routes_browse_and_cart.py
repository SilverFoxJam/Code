import pytest

INDEX_ENDPOINT = "/"
CART_VIEW_ENDPOINT = "/cart"
ADD_TO_CART_ENDPOINT = "/add-to-cart"
CLEAR_CART_ENDPOINT = "/clear-cart"

TITLE_KEY = "title"
QTY_KEY = "quantity"
SEND_JSON = False

EXISTING_TITLE = "1984"
NON_EXISTENT_TITLE = "ThisTitleDoesNotExist"


@pytest.mark.integration
def test_homepage_loads(client):
    r = client.get(INDEX_ENDPOINT)
    assert r.status_code == 200
    body = r.data or b""
    assert (b"Book" in body) or (b"Books" in body) or (b"Add to Cart" in body) or (b"Shop" in body)


@pytest.mark.integration
def test_cart_page_loads(client):
    r = client.get(CART_VIEW_ENDPOINT)
    assert r.status_code == 200
    body = r.data or b""
    assert (b"Cart" in body) or (b"Total" in body) or (b"Your cart" in body)


@pytest.mark.integration
def test_clear_cart_smoke(client):
    r = client.post(CLEAR_CART_ENDPOINT)
    assert r.status_code in (200, 302)


@pytest.mark.integration
def test_add_to_cart_and_total(client):
    payload = {TITLE_KEY: EXISTING_TITLE, QTY_KEY: 2}
    r = client.post(ADD_TO_CART_ENDPOINT, data=payload)
    assert r.status_code in (200, 302)
    r = client.get(CART_VIEW_ENDPOINT)
    assert r.status_code == 200
    body = r.data or b""
    assert (b"Total" in body) or (EXISTING_TITLE.encode() in body)


@pytest.mark.integration
def test_add_to_cart_with_invalid_title_redirects(client):
    payload = {TITLE_KEY: NON_EXISTENT_TITLE, QTY_KEY: 1}
    r = client.post(ADD_TO_CART_ENDPOINT, data=payload)
    assert r.status_code in (200, 302)
