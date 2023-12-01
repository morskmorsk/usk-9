# class ShoppingCartDetail(models.Model):
#     cart = models.ForeignKey(ShoppingCart, related_name='details', on_delete=models.CASCADE)
#     product = models.ForeignKey(Product, on_delete=models.CASCADE)
#     quantity = models.IntegerField(default=1, validators=[MinValueValidator(1)])
#     price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(10)])   
#     discount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
#     added_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     def item_tax(self):
#         try:
#             product_department = self.product.department
#             if product_department.taxable:
#                 return self.price * self.quantity * TAX_RATE  # TAX_RATE is a Decimal object
#             else:
#                 return Decimal('0.00')
#         except:
#             return Decimal('0.00')

#     def item_subtotal(self):
#         try:
#             return (self.price * self.quantity)
#         except:
#             return Decimal('999.99')
    
#     def item_total(self):
#         try:
#             return self.item_subtotal() + self.item_tax()
#         except:
#             return Decimal('99999.99')

import pytest
from decimal import Decimal
from django.utils import timezone
from store.models import ShoppingCartDetail

@pytest.mark.django_db
def test_shopping_cart_detail_model(test_shopping_cart, test_product):
    cart = test_shopping_cart
    product = test_product
    quantity = 2
    price = Decimal('10.00')
    discount = Decimal('0.00')
    # added_at = timezone.now()
    # updated_at = timezone.now()

    cart_detail = ShoppingCartDetail.objects.create(
        cart=cart,
        product=product,
        quantity=quantity,
        price=price,
        discount=discount,
        # added_at=added_at,
        # updated_at=updated_at,
    )

    assert cart_detail.cart == cart
    assert cart_detail.product == product
    assert cart_detail.quantity == quantity
    assert cart_detail.price == price
    assert cart_detail.discount == discount
    # assert cart_detail.added_at == added_at
    # assert cart_detail.updated_at == updated_at
    # assert cart_detail.item_subtotal() == Decimal('20.00')
    assert str(cart_detail) == f"Item: {cart_detail.product.name} in Cart {cart_detail.cart.id} - Quantity: {cart_detail.quantity}"
    # assert cart_detail.item_tax() == Decimal('1.80')
    # assert cart_detail.item_total() == Decimal('21.80')
    