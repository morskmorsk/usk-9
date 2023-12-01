# class AddToCartView(LoginRequiredMixin, View):
#     def post(self, request, *args, **kwargs):
#         try:
#             product = get_object_or_404(Product, id=kwargs.get('product_id'))
#             with transaction.atomic():
#                 cart, created = ShoppingCart.objects.get_or_create(user=request.user)
#                 cart_detail = ShoppingCartDetail.objects.create(
#                     cart=cart,
#                     product=product,
#                     price=request.POST.get('price'),
#                     quantity=1
#                 )
#                 cart_detail.save()
#         except IntegrityError as e:
#             messages.error(request, f"Error adding product to cart: {e}")
#             # Redirect to the previous page or a specific error page
#             return redirect(request.META.get('HTTP_REFERER', 'product-detail'), product_id=product.id)
#         except Exception as e:
#             messages.error(request, f"An unexpected error occurred: {e}")
#             # Redirect to an error page or home page
#             return redirect('home')

#         return redirect('cart')

from django.urls import reverse
import pytest


@pytest.mark.django_db
def test_add_to_cart_view(client, test_user, test_product):
    client.force_login(test_user('testuser'))
    response = client.post(
        reverse('add_to_cart', kwargs={'product_id': test_product.id}),
        {'price': test_product.price}
    )
    assert response.status_code == 302
    assert response.url == reverse('cart')
