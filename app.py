from flask import Flask, render_template, request, redirect, url_for, session
import json
from datetime import datetime

# initialize flask application
app = Flask(__name__)
# Set secret key for session encryption
# in produciton, should be secure, random key stored in environment variables
app.secret_key = 'your_secret_key'  # In production, use a secure random key

# Our "database" of sock products
socks = {
    1: {
        'id': 1,
        'name': 'Meme Lord',
        'description': 'Custom socks with your favorite internet meme',
        'base_price': 12.99,
        'image': 'meme_socks.jpg',
        'category': 'funny'
    },
    2: {
        'id': 2,
        'name': 'Campus Pride',
        'description': 'Show your school spirit with custom logo socks',
        'base_price': 14.99,
        'image': 'campus_socks.jpg',
        'category': 'school'
    },
    3: {
        'id': 3,
        'name': 'Quote Master',
        'description': 'Custom socks with your favorite quote or inside joke',
        'base_price': 13.99,
        'image': 'quote_socks.jpg',
        'category': 'funny'
    }
}


# Function to get available socks
def get_available_products(category=None):
    # retrieve products from database, optionally filtered by category
    if category: # use list comprehension to filter products by category
        return [product for product in socks.values() if product['category'] == category]
    # if no category specified - return all products
    return list(socks.values())


# Function to get a specific sock by ID
# look up single product by ID - returns the product dictionary if found, none otherwise
def get_product_by_id(product_id):
    return socks.get(int(product_id)) # convert to int in case return a string ID


# Function to get all categories
# return list alphabetically sorted
def get_all_categories():
    # use a set to automatically handle uniqueness
    categories = set()
    for product in socks.values():
        categories.add(product['category'])
        # convert set to sorted list before returning
    return list(categories)

# Session Management
# Use Flask's session object to maintain a shopping cart between requests
# The session is stored in an encrypted cookie on the client side

# Initialize shopping cart in session
@app.before_request
def before_request():
    # initialize shopping cart in session if it does not exist
    # this decorator makes this function run before each request
    if 'cart' not in session:
        # initialize empty list if no cart exists in session
        session['cart'] = []

# Application Routes
# these define the different pages/endpoints of the web application
# Each route handles a specific URL and HTTP method
# route for the home page
# home() function sets up the home page so it gets the products and the categories
# then adds them to the index.html file that serves as the template for the homepage
@app.route('/')
def home():
    # homepage route - display all products with optional category filtering

    # get category filter from query parameters
    category = request.args.get('category')
    # get filtered or all products
    products = get_available_products(category)
    # get all categories for the filter UI
    categories = get_all_categories()
    # Render template with all required data
    return render_template('index.html', products=products, categories=categories, current_category=category)

# route for the products page
# product_detail() function sets up the product detail page
# It displats the info for a specific product ID
@app.route('/product/<int:product_id>')
def product_detail(product_id):
    product = get_product_by_id(product_id)
    if not product:
        return redirect(url_for('home'))
    return render_template('product_detail.html', product=product)

# route for the add to cart page
# add_to_cart function sets up the add to cart page - w/ product id, quantity, and text
# the user wants to add
@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    # handle adding items to the shopping cart
    # only accepts POST requests with form data containing: product_id, quantity, custom_text
    # return - redirect tothe cart page after adding the items

    # get form data with defaults
    product_id = int(request.form.get('product_id'))
    quantity = int(request.form.get('quantity', 1)) # default to 1 if not specified
    custom_text = request.form.get('custom_text', '')
    # verify if the product exists
    product = get_product_by_id(product_id)
    if not product:
        return redirect(url_for('home'))

    # create cart item dictionary
    cart_item = {
        'product_id': product_id,
        'name': product['name'],
        'price': product['base_price'],
        'quantity': quantity,
        'custom_text': custom_text,
        # calculate the line total
        'total': product['base_price'] * quantity
    }
    # get current cart from session
    cart = session.get('cart', [])
    # add new item to cart
    cart.append(cart_item)
    # store updated cart in session
    session['cart'] = cart

    # redirect to cart page to show results
    return redirect(url_for('cart'))

# last route and page to set up - the cart page
# after adding product to cart - routed to see their cart and socks in it
# the cart() function sets up the cart page, and gets the cart with the items
# for the current session (browser session)
@app.route('/cart')
def cart():
    # display the shopping cart with all items and total cost

    # get cart from session (default to empty list if not exists)
    cart = session.get('cart', [])
    # calculate grand total by summing all item totals
    total = sum(item['total'] for item in cart)
    # render cart template with data
    return render_template('cart.html', cart=cart, total=total)

# check out routes
@app.route('/checkout')
def checkout():
    #
    cart = session.get('cart', [])
    if not cart:
        return redirect(url_for('home'))

    total = sum(item['total'] for item in cart)
    return render_template('checkout.html', cart=cart, total=total)

@app.route('/complete_order', methods=['POST'])
def complete_order():
    # get customer information
    name = request.form.get('name')
    email = request.form.get('email')

    # clear the cart
    session['cart'] = []

    # Show thank you page
    return render_template('thank_you.html', name=name, email=email)

# Application Entry Point
# this runs when the script is executed directly, not imported as a module

# main function - always have in python
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')