import pytest
from app import cart

INDEX_ENDPOINT = "/"
CART_VIEW_ENDPOINT = "/cart"
ADD_TO_CART_ENDPOINT = "/add-to-cart"
UPDATE_CART_ENDPOINT = "/update-cart"
REMOVE_FROM_CART_ENDPOINT = "/remove-from-cart"
CHECKOUT_ENDPOINT = "/checkout"

TITLE_KEY = "title"
QTY_KEY = "quantity"

EXISTING_TITLE = "1984"
ANOTHER_TITLE = "The Great Gatsby"


@pytest.mark.integration
def test_update_cart_changes_quantity(client):
    cart.clear()
    r = client.post(ADD_TO_CART_ENDPOINT, data={TITLE_KEY: EXISTING_TITLE, QTY_KEY: 1})
    assert r.status_code in (200, 302)
    r = client.post(UPDATE_CART_ENDPOINT, data={TITLE_KEY: EXISTING_TITLE, QTY_KEY: 5})
    assert r.status_code in (200, 302)
    assert cart.get_total_items() == 5
    r = client.get(CART_VIEW_ENDPOINT)
    assert r.status_code == 200


@pytest.mark.integration
def test_update_cart_zero_removes_item(client):
    cart.clear()
    client.post(ADD_TO_CART_ENDPOINT, data={TITLE_KEY: EXISTING_TITLE, QTY_KEY: 2})
    r = client.post(UPDATE_CART_ENDPOINT, data={TITLE_KEY: EXISTING_TITLE, QTY_KEY: 0})
    assert r.status_code in (200, 302)
    assert cart.get_total_items() == 0
    assert cart.is_empty()


@pytest.mark.integration
def test_remove_from_cart_removes_by_title(client):
    cart.clear()
    client.post(ADD_TO_CART_ENDPOINT, data={TITLE_KEY: EXISTING_TITLE, QTY_KEY: 1})
    client.post(ADD_TO_CART_ENDPOINT, data={TITLE_KEY: ANOTHER_TITLE, QTY_KEY: 2})
    assert cart.get_total_items() == 3
    r = client.post(REMOVE_FROM_CART_ENDPOINT, data={TITLE_KEY: ANOTHER_TITLE})
    assert r.status_code in (200, 302)
    titles = list(cart.items.keys())
    assert ANOTHER_TITLE not in titles
    assert cart.get_total_items() == 1


@pytest.mark.integration
def test_checkout_page_loads(client):
    r = client.get(CHECKOUT_ENDPOINT)
    assert r.status_code in (200, 302)