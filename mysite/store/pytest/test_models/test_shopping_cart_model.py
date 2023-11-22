import pytest
from decimal import Decimal
from store.models import ShoppingCart

# tests for ShoppingCart model
@pytest.mark.django_db
def test_shopping_cart_model(new_user_profile):
    """ Test ShoppingCart model """
    user = new_user_profile('testuser')
    shopping_cart = ShoppingCart.objects.create(
        customer=user,
    )
    assert shopping_cart.customer == user
    assert str(shopping_cart) == f"Shopping Cart for {user.user.username}"

# tests for ShoppingCart model methods
