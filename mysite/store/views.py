from typing import Any
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, FormView, TemplateView
from django.shortcuts import redirect, get_object_or_404, render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
import logging
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from .forms import UserForm
from django.contrib.auth import login
from django.views import View
from .models import Product, ShoppingCart, ShoppingCartDetail
from django.core.exceptions import ObjectDoesNotExist

from .models import Product

logger = logging.getLogger(__name__)


class ProductListView(LoginRequiredMixin,ListView):
    model = Product
    template_name = 'store/product_list.html'
    context_object_name = 'products'

    class Meta:
        ordering = ['-id']
        plural_name = 'Products'


class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Product
    template_name = 'store/product_detail.html'
    context_object_name = 'product'


class RegisterView(FormView):
    template_name = 'registration/register.html'
    form_class = UserForm
    success_url = reverse_lazy('home')  # Redirect to home or another appropriate page

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)  # Log in the user immediately after signup
        return super().form_valid(form)
    
    def form_invalid(self, form):
        return super().form_invalid(form)


class AddToCartView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        product = get_object_or_404(Product, id=kwargs.get('product_id'))
        cart, created = ShoppingCart.objects.get_or_create(user=request.user)
        cart_detail, created = ShoppingCartDetail.objects.get_or_create(
            cart=cart,
            product=product,
            price=request.POST.get('price'),
            defaults={'quantity': 1},
        )
        if not created:
            cart_detail.quantity += 1
        cart_detail.save()
        return redirect('cart')  # Redirect to product list or cart page
    


class ShoppingCartDetailListView(LoginRequiredMixin, ListView):
    model = ShoppingCartDetail
    template_name = 'store/shopping_cart_list.html'
    context_object_name = 'shopping_cart_items'

    def get_queryset(self):
        return self.model.objects.filter(cart__user=self.request.user)