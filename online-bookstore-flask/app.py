from flask import Flask, render_template, request, redirect, url_for, flash
from models import Book, Cart

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for session management


# Create a cart instance to manage the cart
cart = Cart()

# Create a global books list to avoid duplication
BOOKS = [
    Book("The Great Gatsby", "Fiction", 10.99, "/images/books/the_great_gatsby.jpg"),
    Book("1984", "Dystopia", 8.99, "/images/books/1984.jpg"),
    Book("I Ching", "Traditional", 18.99, "/images/books/I-Ching.jpg"),
    Book("Moby Dick", "Adventure", 12.49, "/images/books/moby_dick.jpg")
]


def get_book_by_title(title):
    """Helper function to find a book by title"""
    return next((book for book in BOOKS if book.title == title), None)


@app.route('/')
def index():
    return render_template('index.html', books=BOOKS, cart=cart)


@app.route('/add-to-cart', methods=['POST'])
def add_to_cart():
    book_title = request.form.get('title')
    quantity = int(request.form.get('quantity', 1))

    book = get_book_by_title(book_title)

    if book:
        cart.add_book(book, quantity)
        flash(f'Added {quantity} "{book.title}" to cart!', 'success')
    else:
        flash('Book not found!', 'error')

    return redirect(url_for('index'))


@app.route('/remove-from-cart', methods=['POST'])
def remove_from_cart():
    book_title = request.form.get('title')
    cart.remove_book(book_title)
    flash(f'Removed "{book_title}" from cart!', 'success')
    return redirect(url_for('view_cart'))


@app.route('/update-cart', methods=['POST'])
def update_cart():
    """
    Update the quantity of a book in the cart.
    This function handles HTTP POST requests to update the quantity of a book in the user's cart.
    If the quantity is set to 0 or less, the book is effectively removed from the cart.
    Args:
        None (uses form data from the request)
    Returns:
        Response: Redirects to the view_cart page after updating the cart.
    Form Parameters:
        title (str): The title of the book to update.
        quantity (int): The new quantity of the book. Defaults to 1.
    Flash Messages:
        - Confirmation of removal if quantity <= 0
        - Confirmation of update otherwise
    """
    book_title = request.form.get('title')
    quantity = int(request.form.get('quantity', 1))

    cart.update_quantity(book_title, quantity)

    if quantity <= 0:
        flash(f'Removed "{book_title}" from cart!', 'success')
    else:
        flash(f'Updated "{book_title}" quantity to {quantity}!', 'success')

    return redirect(url_for('view_cart'))


@app.route('/cart')
def view_cart():
    return render_template('cart.html', cart=cart)


@app.route('/clear-cart', methods=['POST'])
def clear_cart():
    cart.clear()
    flash('Cart cleared!', 'success')
    return redirect(url_for('view_cart'))


@app.route('/checkout')
def checkout():
    if cart.is_empty():
        flash('Your cart is empty!', 'error')
        return redirect(url_for('index'))

    total_price = cart.get_total_price()
    return render_template('checkout.html', cart=cart, total_price=total_price)


if __name__ == '__main__':
    app.run(debug=True)
