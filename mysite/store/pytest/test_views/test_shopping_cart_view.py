# class ShoppingCartView(LoginRequiredMixin, DetailView):
#     model = ShoppingCart
#     template_name = 'store/shopping_cart_list.html'  # replace with your actual template path

#     def get_object(self, queryset=None):
#         return ShoppingCart.objects.get(user=self.request.user)
        
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         cart = self.get_object()
#         context['cart'] = {
#             'subtotal': cart.calculate_subtotal(),
#             'tax': cart.calculate_tax(),
#             'total': cart.calculate_total(),
#         }
#         return context

from django.urls import reverse
import pytest

from store.models import ShoppingCart


@pytest.mark.django_db
def test_shopping_cart_view(client, test_user, test_shopping_cart):
    user = test_user('testuser')
    ShoppingCart.objects.create(user=user)
    client.force_login(user)
    response = client.get(reverse('cart'))
    assert response.status_code == 200
    assert 'cart' in response.context
    assert response.context['cart']['subtotal'] == 0
    assert response.context['cart']['tax'] == 0
    assert response.context['cart']['total'] == 0
    # assert response.context['cart']['items'] == []
    # assert response.context['cart']['count'] == 0
