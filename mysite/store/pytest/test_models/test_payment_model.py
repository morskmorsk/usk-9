import pytest
from django.utils import timezone
from django.contrib.auth.models import User
from store.models import Payment


# Test for creating a Payment instance
@pytest.mark.django_db
def test_create_payment(test_user):
    transaction_id = "TXN123456"
    payment_method = "Credit Card"
    payment_gateway = "Stripe"
    payment_type = "Online"
    amount = 100.00
    payment_status = "pending"

    payment = Payment.objects.create(
        user=test_user,
        transaction_id=transaction_id,
        payment_method=payment_method,
        payment_gateway=payment_gateway,
        payment_type=payment_type,
        amount=amount,
        payment_status=payment_status
    )

    assert payment.user == test_user
    assert payment.transaction_id == transaction_id
    assert payment.payment_method == payment_method
    assert payment.payment_gateway == payment_gateway
    assert payment.payment_type == payment_type
    assert payment.amount == amount
    assert payment.payment_status == payment_status
    assert payment.created_at <= timezone.now()
    assert payment.updated_at <= timezone.now()

# @pytest.mark.django_db
# def test_payment_str(test_user):
#     payment = Payment.objects.create(
#         user=test_user,
#         transaction_id="TXN789123",
#         payment_method="PayPal",
#         amount=50.00,
#         payment_status="completed"
#     )
#     expected_str = f"Payment {payment.id} - {payment.payment_status}"
#     assert str(payment) == expected_str
