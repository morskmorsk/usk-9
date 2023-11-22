import pytest
from django.utils import timezone
from decimal import Decimal
from store.models import Order, Product, OrderDetail, Supplier, Location, Inventory, Department, Return
from phonenumber_field.modelfields import PhoneNumberField
import uuid


@pytest.mark.django_db
def test_return_model(test_return, order, test_product):
    return_obj = test_return
    assert return_obj.order == order
    assert return_obj.product == test_product
    assert return_obj.user == test_return.user
    assert return_obj.condition == 'Test condition'
    assert return_obj.reason == 'Test reason'

@pytest.mark.django_db
def test_return_model_str(test_return):
    return_obj = test_return
    assert str(return_obj) == f"Return for {return_obj.product.name} by {return_obj.user.user.username} - Condition: {return_obj.condition}"
