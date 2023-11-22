import pytest
from conftest import new_user_profile, new_user, order
from django.utils import timezone
from store.models import Order
# import uuid


@pytest.mark.django_db
def test_create_order(new_user_profile):
    order_date = timezone.now()
    user = new_user_profile('testuser2')
    order = Order.objects.create(
        user=user,
        order_date=order_date,
    )

    assert order.user == user
    assert order.order_date == order_date
    assert order.status == 'pending'


# Test for string representation of Order
@pytest.mark.django_db
def test_order_str(order):
    expected_str = f"Order {order.id} - Status: {order.status}"
    assert str(order) == expected_str