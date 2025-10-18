import pytest
from timeit import timeit
from models import Book, Cart


@pytest.mark.perf
def test_cart_total_under_1ms():
    cart = Cart()
    for i in range(50):
        cart.add_book(Book(f"Book{i}", "Cat", 9.99, f"/i{i}.jpg"), 1)
    cart.get_total_price()
    t = timeit(lambda: cart.get_total_price(), number=1000)
    avg_ms = (t / 1000) * 1000.0
    assert avg_ms < 1.0
