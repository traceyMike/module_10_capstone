from app import app

def test_empty_cart_checkout_redirect():
    # test that users with empty carts are redirected from checkout
    # create a test client
    with app.test_client() as client:
        # set up an empty cart in the session
        with client.session_transaction() as session:
            session['cart'] = []

        # try to access checkout page
        response = client.get('/checkout', follow_redirects=True)

        # should redirect to home page
        assert response.request.path == '/'