import pytest
from decimal import Decimal
from store.models import ShoppingCart

# tests for ShoppingCart model
@pytest.mark.django_db
def test_shopping_cart_model(test_user):
    user = test_user('testuser')
    shopping_cart = ShoppingCart.objects.create(
        user=user,
    )
    assert shopping_cart.user == user
    assert str(shopping_cart) == f"Shopping Cart for {user.username}"

# tests for ShoppingCart model methods
