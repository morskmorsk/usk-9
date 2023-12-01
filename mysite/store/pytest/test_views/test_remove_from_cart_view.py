# remove from cart view:
# class RemoveFromCartDetailView(LoginRequiredMixin, DeleteView):
#     def post(self, request, *args, **kwargs):
#         cart_detail = get_object_or_404(ShoppingCartDetail, id=kwargs.get('detail_id'))
#         cart_detail.delete()
#         return redirect('cart')

# cart detail view:
# class ShoppingCartDetail(models.Model):
#     cart = models.ForeignKey(ShoppingCart, related_name='details', on_delete=models.CASCADE)
#     product = models.ForeignKey(Product, on_delete=models.CASCADE)
#     quantity = models.IntegerField(default=1, validators=[MinValueValidator(1)])
#     price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(10)])   
#     discount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
#     added_at = models.DateTimeField(auto_now_add=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
    
#     def item_tax(self):
#         try:
#             product_department = self.product.department
#             if product_department.taxable:
#                 return self.price * TAX_RATE  # TAX_RATE is a Decimal object
#             else:
#                 return Decimal('0.00')
#         except:
#             return Decimal('999.99')

#     def item_total(self):
#         try:
#             return self.price + self.item_tax()
#         except:
#             return Decimal('999.99')

#     def __str__(self):
#         return f"Item: {self.product.name} in Cart {self.cart.id} - Quantity: {self.quantity}"

#     class Meta:
#         verbose_name_plural = 'Shopping Cart Details'
#         ordering = ['id']


import pytest
from django.urls import reverse
from decimal import Decimal

from store.models import Product, ShoppingCart, ShoppingCartDetail, Department, Location

@pytest.mark.django_db
def test_remove_from_cart_view(client, django_user_model):
    # Create test user
    user = django_user_model.objects.create_user(username='testuser', password='12345')
    
    # Create necessary related objects
    department = Department.objects.create(name='Test Department', description='Test Department Description', taxable=True)
    location = Location.objects.create(name='Test Location', address='Test Address')
    
    # Create a product with required foreign keys
    product = Product.objects.create(
        name='Test Product',
        price=Decimal('10.00'),
        department=department,
        location=location,
        # Other fields as required
    )

    # Create a shopping cart and detail
    cart = ShoppingCart.objects.create(user=user)
    cart_detail = ShoppingCartDetail.objects.create(
        cart=cart,
        product=product,
        quantity=1,
        price=Decimal('10.00')
        # Other fields as required
    )

    # Authenticate the user and perform the action
    client.force_login(user)
    response = client.post(reverse('remove_from_cart', kwargs={'detail_id': cart_detail.id}))

    # Assertions
    assert response.status_code == 302
    assert response.url == reverse('cart')
    assert ShoppingCartDetail.objects.count() == 0
    assert ShoppingCart.objects.count() == 1
    assert Product.objects.count() == 1
