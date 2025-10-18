import os
import sys
import cProfile
import io
import pstats

ROOT = os.path.dirname(os.path.dirname(__file__))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from models import Book, Cart  # noqa: E402


def main():
    cart = Cart()
    # build a bigger cart to profile work under load
    for i in range(5000):
        cart.add_book(Book(f"B{i}", "Cat", 9.99, f"/i{i}.jpg"), 1)
    # profile the total computation many times
    for _ in range(200):
        cart.get_total_price()


if __name__ == "__main__":
    os.makedirs("artifacts/perf", exist_ok=True)
    prof_path = "artifacts/perf/profile_cart.prof"
    txt_path = "artifacts/perf/profile_cart.txt"

    cProfile.run("main()", prof_path)

    buf = io.StringIO()
    ps = pstats.Stats(prof_path, stream=buf)
    ps.sort_stats("tottime").print_stats(20)

    with open(txt_path, "w", encoding="utf-8") as f:
        f.write(buf.getvalue())

    print("=== PROFILE (top 20 by tottime) ===")
    print(buf.getvalue())
    print(f"\nWritten: {prof_path} and {txt_path}")
