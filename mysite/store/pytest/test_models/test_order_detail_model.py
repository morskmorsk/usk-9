import pytest
from decimal import Decimal
from store.models import OrderDetail
from conftest import order, test_product


# class OrderDetail(models.Model):
#     order = models.ForeignKey(Order, related_name='details', on_delete=models.CASCADE)
#     product = models.ForeignKey(Product, on_delete=models.CASCADE)
#     quantity = models.IntegerField(default=1)
#     price = models.DecimalField(max_digits=10, decimal_places=2)

#     def subtotal(self):
#         return self.price * self.quantity

#     def __str__(self):
#         return f"Detail for Order {self.order.id} - Product: {self.product.name}"


@pytest.mark.django_db
def test_order_detail_subtotal(order, test_product):
    order_detail = OrderDetail.objects.create(
        order=order,
        product=test_product,
        quantity=3,
        price=Decimal('10.00')
    )
    assert order_detail.subtotal() == Decimal('30.00')


@pytest.mark.django_db
def test_order_detail_str(order, test_product):
    order_detail = OrderDetail.objects.create(
        order=order,
        product=test_product,
        quantity=3,
        price=Decimal('10.00')
    )
    assert str(order_detail) == f"Detail for Order {order.id} - Product: {test_product.name}"


@pytest.mark.django_db
def test_order_detail_order(order, test_product):
    order_detail = OrderDetail.objects.create(
        order=order,
        product=test_product,
        quantity=3,
        price=Decimal('10.00')
    )
    assert order_detail.order == order


@pytest.mark.django_db
def test_order_detail_product(order, test_product):
    order_detail = OrderDetail.objects.create(
        order=order,
        product=test_product,
        quantity=3,
        price=Decimal('10.00')
    )
    assert order_detail.product == test_product


@pytest.mark.django_db
def test_order_detail_quantity(order, test_product):
    order_detail = OrderDetail.objects.create(
        order=order,
        product=test_product,
        quantity=3,
        price=Decimal('10.00')
    )
    assert order_detail.quantity == 3


@pytest.mark.django_db
def test_order_detail_price(order, test_product):
    order_detail = OrderDetail.objects.create(
        order=order,
        product=test_product,
        quantity=3,
        price=Decimal('10.00')
    )
    assert order_detail.price == Decimal('10.00')
