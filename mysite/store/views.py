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
from django.http import Http404
from django.db import IntegrityError, transaction
from django.contrib import messages
from django.contrib.auth.models import User

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
        cart, created = ShoppingCart.objects.get_or_create(user=user)
        return super().form_valid(form)
    
    def form_invalid(self, form):
        return super().form_invalid(form)


class AddToCartView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        try:
            product = get_object_or_404(Product, id=kwargs.get('product_id'))
            with transaction.atomic():
                cart, created = ShoppingCart.objects.get_or_create(user=request.user)
                cart_detail = ShoppingCartDetail.objects.create(
                    cart=cart,
                    product=product,
                    price=request.POST.get('price'),
                    quantity=1
                )
                cart_detail.save()
        except IntegrityError as e:
            messages.error(request, f"Error adding product to cart: {e}")
            # Redirect to the previous page or a specific error page
            return redirect(request.META.get('HTTP_REFERER', 'product-detail'), product_id=product.id)
        except Exception as e:
            messages.error(request, f"An unexpected error occurred: {e}")
            # Redirect to an error page or home page
            return redirect('home')

        return redirect('cart')
    

class ShoppingCartView(LoginRequiredMixin, DetailView):
    model = ShoppingCart
    template_name = 'store/shopping_cart_list.html'  # replace with your actual template path

    def get_object(self, queryset=None):
        return ShoppingCart.objects.get(user=self.request.user)
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart = self.get_object()
        context['cart'] = {
            'subtotal': cart.calculate_subtotal(),
            'tax': cart.calculate_tax(),
            'total': cart.calculate_total(),
        }
        return context


class RemoveFromCartDetailView(LoginRequiredMixin, DeleteView):
    def post(self, request, *args, **kwargs):
        cart_detail = get_object_or_404(ShoppingCartDetail, id=kwargs.get('detail_id'))
        cart_detail.delete()
        return redirect('cart')
    

class CartDetailUpdatePriceView(LoginRequiredMixin, UpdateView):
    model = ShoppingCartDetail
    fields = ['price']
    template_name = 'store/cart_detail_update.html'
    success_url = reverse_lazy('cart')

    def get_object(self, queryset=None):
        return ShoppingCartDetail.objects.get(id=self.kwargs.get('detail_id'))


class CheckOutView(LoginRequiredMixin, TemplateView):
    template_name = 'store/checkout.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart = ShoppingCart.objects.get(user=self.request.user)
        context['cart'] = {
            'subtotal': cart.calculate_subtotal(),
            'tax': cart.calculate_tax(),
            'total': cart.calculate_total(),
        }
        return context



class UpdateUserProfileView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = User
    fields = ['first_name', 'last_name', 'email']
    template_name = 'store/user_profile_update.html'
    success_url = reverse_lazy('home')
    success_message = 'Profile successfully updated!'

    def get_object(self, queryset=None):
        return self.request.user