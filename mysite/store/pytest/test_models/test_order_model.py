import pytest
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from store.models import Order, UserProfile, Payment
from decimal import Decimal
# ///////////////////////////////////////////
# # Fixture for UserProfile
# @pytest.fixture
# def user_profile(db):
#     user = User.objects.create_user(username='testuser', password='testpass123')
#     return UserProfile.objects.create(user=user)
# ///////////////////////////////////////////
User = get_user_model()

@pytest.fixture
def new_user(db):
    def create_user(username):
        # Ensure uniqueness by deleting any existing user with the same username
        User.objects.filter(username=username).delete()
        return User.objects.create_user(username=username, password='testpass123')
    return create_user
# ///////////////////////////////////////////
# Fixture for Payment
@pytest.fixture
def payment(db, user_profile):
    return Payment.objects.create(
        user=user_profile,
        transaction_id="TXN12345",
        payment_method="Credit Card",
        amount=Decimal("100.00"),
        payment_status="completed"
    )

# Test for creating an Order instance
@pytest.mark.django_db
def test_create_order(user_profile, payment):
    order = Order.objects.create(
        user=user_profile,
        status="pending",
        shipping_address="123 Main St",
        shipping_city="Anytown",
        shipping_state="NY",
        shipping_zip_code="12345",
        shipping_phone="+1234567890",
        shipping_method="UPS",
        shipping_cost=Decimal("10.00"),
        tax=Decimal("7.00"),
        total=Decimal("117.00"),
        payment=payment
    )

    assert order.user == user_profile
    assert order.status == "pending"
    assert order.shipping_address == "123 Main St"
    assert order.shipping_method == "UPS"
    assert order.shipping_cost == Decimal("10.00")
    assert order.tax == Decimal("7.00")
    assert order.total == Decimal("117.00")
    assert order.payment == payment

# Test for string representation of Order
@pytest.mark.django_db
def test_order_str(user_profile, payment):
    order = Order.objects.create(
        user=user_profile,
        status="shipped",
        payment=payment
    )
    expected_str = f"Order {order.id} - Status: {order.status}"
    assert str(order) == expected_str

# Test for Order subtotal, tax, and total calculations
@pytest.mark.django_db
def test_order_calculations(user_profile, payment):
    order = Order.objects.create(
        user=user_profile,
        status="pending",
        shipping_cost=Decimal("10.00"),
        payment=payment
    )
    # Assuming 'details' is a related_name for items in the order
    # Add test items to the order here...

    # Test the subtotal, tax, and total methods
    assert order.subtotal() == sum(item.product.price * item.quantity for item in order.details.all())
    assert order.tax() == order.subtotal() * Decimal("0.07")
    assert order.total() == order.subtotal() + order.tax() + order.shipping_cost
