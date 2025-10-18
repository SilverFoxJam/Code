import math
from decimal import Decimal, ROUND_HALF_UP
import pytest

from models import Book, Cart, CartItem  # matches your models.py


def to_money(x):
    return (Decimal(str(x))).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def get_cart_total(cart: Cart):
    if hasattr(cart, "get_total_price"):
        return to_money(cart.get_total_price())
    if hasattr(cart, "items"):
        total = Decimal("0.00")
        for item in cart.items.values():
            total += Decimal(str(item.get_total_price()))
        return to_money(total)
    raise pytest.skip("Cart total not accessible via known methods/attrs.")


@pytest.fixture
def sample_books():
    b1 = Book("Unit Testing in Python", "Tech", 10.00, "/images/b1.jpg")
    b2 = Book("Clean Design", "Tech", 5.99, "/images/b2.jpg")
    return b1, b2


def test_book_fields(sample_books):
    b1, b2 = sample_books
    assert b1.title and b1.category and hasattr(b1, "price")
    assert isinstance(b1.price, (int, float))
    assert b2.title == "Clean Design"
    assert math.isclose(b2.price, 5.99, rel_tol=0, abs_tol=1e-9)


def test_add_book_accumulates_quantity_and_total(sample_books):
    cart = Cart()
    b1, b2 = sample_books

    cart.add_book(b1, 2)
    cart.add_book(b2, 3)

    expected = to_money(2 * b1.price + 3 * b2.price)
    assert get_cart_total(cart) == expected
    assert cart.get_total_items() == 5

    cart.add_book(b1, 1)
    expected = to_money(3 * b1.price + 3 * b2.price)
    assert get_cart_total(cart) == expected
    assert cart.get_total_items() == 6


def test_update_quantity_and_remove_behaviour(sample_books):
    cart = Cart()
    b1, b2 = sample_books

    cart.add_book(b1, 2)
    cart.add_book(b2, 1)
    assert get_cart_total(cart) == to_money(2 * b1.price + 1 * b2.price)

    cart.update_quantity(b1.title, 5)
    assert get_cart_total(cart) == to_money(5 * b1.price + 1 * b2.price)
    assert cart.get_total_items() == 6

    cart.update_quantity(b2.title, 0)
    assert get_cart_total(cart) == to_money(5 * b1.price)
    assert cart.get_total_items() == 5
    assert b2.title not in cart.items

    cart.remove_book(b1.title)
    assert get_cart_total(cart) == to_money(0)
    assert cart.get_total_items() == 0
    assert cart.is_empty()


def test_clear_cart_sets_total_to_zero(sample_books):
    cart = Cart()
    b1, b2 = sample_books
    cart.add_book(b1, 2)
    cart.add_book(b2, 3)
    assert get_cart_total(cart) == to_money(2 * b1.price + 3 * b2.price)
    assert not cart.is_empty()

    cart.clear()
    assert get_cart_total(cart) == to_money(0)
    assert cart.is_empty()


def test_get_items_returns_cartitem_list(sample_books):
    cart = Cart()
    b1, b2 = sample_books
    cart.add_book(b1, 2)
    cart.add_book(b2, 1)

    items = cart.get_items()
    assert isinstance(items, list)
    assert all(isinstance(it, CartItem) for it in items)
    first = items[0]
    assert hasattr(first, "book") and hasattr(first, "quantity")
    assert isinstance(first.quantity, int)


def test_items_dict_structure_and_totals(sample_books):
    cart = Cart()
    b1, b2 = sample_books

    cart.add_book(b1, 2)
    cart.add_book(b2, 3)

    assert b1.title in cart.items and b2.title in cart.items
    assert isinstance(cart.items[b1.title], CartItem)
    total_2 = to_money(cart.items[b2.title].get_total_price())
    assert total_2 == to_money(3 * b2.price)

    calc_sum = to_money(sum(Decimal(str(ci.get_total_price())) for ci in cart.items.values()))
    assert get_cart_total(cart) == calc_sum