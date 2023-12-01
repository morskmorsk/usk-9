# class RemoveFromCartDetailView(LoginRequiredMixin, DeleteView):
#     def post(self, request, *args, **kwargs):
#         cart_detail = get_object_or_404(ShoppingCartDetail, id=kwargs.get('detail_id'))
#         cart_detail.delete()
#         return redirect('cart')

import pytest
from django.urls import reverse

