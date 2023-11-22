import pytest
from django.utils import timezone
from decimal import Decimal
from store.models import Order, UserProfile, Product, OrderDetail, Supplier, Location, Inventory, Department, Return
from phonenumber_field.modelfields import PhoneNumberField
import uuid


# create test_return_model.py
# class Return(models.Model):
#     order = models.ForeignKey(Order, on_delete=models.CASCADE)
#     product = models.ForeignKey(Product, on_delete=models.CASCADE)
#     user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
#     reason = models.TextField(blank=True, null=True)
#     return_date = models.DateTimeField(default=timezone.now)
#     condition = models.CharField(max_length=255)
#     restocking_fee = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
#     refund_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
#     condition = models.CharField(max_length=255, choices=CONDITION_CHOICES)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#     refund_processed = models.BooleanField(default=False)
#     refund_transaction_id = models.CharField(max_length=255, blank=True, null=True)

    # def save(self, *args, **kwargs):
    #     if not self.pk:  # Check if the return is new; if so, calculate restocking fee
    #         self.restocking_fee = self.product.price * 0.15
    #     super(Return, self).save(*args, **kwargs)
    #     # You would typically also update inventory and process the refund here, depending on your workflow

    # def __str__(self):
    #     return f"Return for {self.product.name} by {self.user.user.username} - Condition: {self.condition}"


@pytest.mark.django_db
def test_return_model(test_return, order, test_product):
    return_obj = test_return
    assert return_obj.order == order
    assert return_obj.product == test_product
    assert return_obj.user == test_return.user
    assert return_obj.condition == 'Test condition'


# @pytest.mark.django_db
# def test_return_model_save(test_return, test_product):
#     return_obj = test_return
#     return_obj.save()
#     assert return_obj.restocking_fee == test_product.price * Decimal(0.15)


@pytest.mark.django_db
def test_return_model_str(test_return):
    return_obj = test_return
    assert str(return_obj) == f"Return for {return_obj.product.name} by {return_obj.user.user.username} - Condition: {return_obj.condition}"
