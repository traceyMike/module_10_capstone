# import the functions to test
from app import get_available_products, get_product_by_id, get_all_categories

# test the get available products function
def test_get_available_products():
    # verify that we can retrieve products
    # call the get_available_products function
    products = get_available_products()

    # test using an assertion if three products were returned
    assert len(products) == 3

    # test that products have all of the required fields (price, description, category, etc)
    assert all('id' in p and 'name' in p and 'description' in p and 'base_price' in p
               and 'image' in p and 'category' in products for p in products)

    # test that the number of products in the 'funny' category = 2
    assert len(get_available_products('funny')) == 2

# test the get product by id function
def test_get_product_by_id():
    # get a product from the collection of products with the product id 1
    product = get_product_by_id(1)

    # test that the product exists and that the ID is 1 and the name is Meme Lord
    assert product and product['id'] == 1 and product['name'] == 'Meme Lord'

    # test that an invalid product id is handled gracefully instead of throwing an error
    assert get_product_by_id(999) is None

# Test the get_all_categories function
def test_get_all_categories():
    # get the categories of sock
    categories = get_all_categories()

    # test that there are two categories in the list
    assert len(categories) == 2

    # Test that the two categories are funny and school
    assert 'funny' in categories and 'school' in categories